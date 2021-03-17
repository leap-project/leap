package coordinator

import (
	"time"
	"context"
	"github.com/sirupsen/logrus"
	"github.com/golang/protobuf/proto"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	pb "leap/proto"
	"leap/utils"
	"io"
)

type ResultFromSite struct {
	Response *pb.MapResponse
	Err      error
	SiteId   int64
}

// Makes a remote procedure call to the cloud algo, so that
// it can execute the specified algorithm.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Compute request specifying the algo to be used.
func (c *Coordinator) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	c.Log.Info("Received compute request.")
	c.ReqCounterMux.Lock()
	req.Id = c.ReqCounter
	currentTime := time.Now().UnixNano()
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Start timing")
	c.ReqCounter++
	c.ReqCounterMux.Unlock()
	err := c.checkSiteBudget(ctx, req)
	checkErr(c, err)
	if err == nil {
		c.Log.Info("Sufficient budget for compute request.")
	} else {
		return nil, err
	}

	conn, err := c.Dial(c.Conf.CloudAlgoIpPort, c.Conf.CloudAlgoCN)

	checkErr(c, err)

	defer conn.Close()

	client := pb.NewCloudAlgoClient(conn)
	response, err := client.Compute(context.Background(), req)

	checkErr(c, err)
	if err == nil {
		c.Log.Info("Successfully returned compute.")
	}

	currentTime = time.Now().UnixNano()
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End timing")
	return response, err
}

// Makes a remote procedure call to a site connector with a
// map request and returns the results of computing the map
// function on multiple sites.
//
// stream: Stream used to receive and send bytes to cloud algo.
func (c *Coordinator) Map(stream pb.Coordinator_MapServer) (err error) {
	// Receive request in chunks
	currentTime := time.Now().UnixNano()
	req, err := receiveMapRequestStream(stream)
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Start receive from cloud algo")
	currentTime = time.Now().UnixNano()
	checkErr(c, err)
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End receive from cloud algo")

	if c.SiteConnectors.Length() == 0 {
		c.Log.WithFields(logrus.Fields{"request-id": req.Id}).Warn("No sites have been registered.")
		return status.Error(codes.Unavailable, "There have been no sites registered.")
	}

	results, err := c.getResultsFromSites(req)

	// Send response in chunks
	currentTime = time.Now().UnixNano()
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Start send to cloud algo")
	err = sendMapResponseStream(&results, stream)
	currentTime = time.Now().UnixNano()
	checkErr(c, err)
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End send to cloud algo")

	return err
}

// Spawns a goroutine that sends a request to each site. The
// responses are then received through a channel and appended
// to the results. The results are returned to the calling
// algorithm in the cloud.
//
// req: The compute request to be sent to each site.
func (c *Coordinator) getResultsFromSites(req *pb.MapRequest) (pb.MapResponses, error) {
	ch := make(chan ResultFromSite)

	sitesLength := 0
	// Asynchronously send compute request to each site.
	for _, siteId := range req.Sites {
		item := c.SiteConnectors.Get(siteId)
		if item != nil {
			site := item.(SiteConnector)
			go c.getResultFromSite(req, site, ch)
			sitesLength++
		}
	}

	// Append the responses to the asynchronous requests
	results := []ResultFromSite{}
	for i := 0; i < sitesLength; i++ {
		select {
		case response := <-ch:
			if response.Err != nil {
				c.Log.WithFields(logrus.Fields{"request-id": req.Id}).Error(response.Err)
			}
			results = append(results, response)
		}
	}

	unavailableSites := getUnavailableSites(results)
	mapResponses := getSuccessfulResponses(results)

	// Determine if there were unavailable sites
	if len(unavailableSites) == sitesLength {
		c.Log.WithFields(logrus.Fields{"unavailable-sites": unavailableSites,
			"request-id": req.Id}).Error("Wasn't able to contact any of the registered sites")
		return mapResponses, status.Error(codes.Unavailable, "Wasn't able to contact any of the registered sites")
	} else if len(unavailableSites) > 0 {
		c.Log.WithFields(logrus.Fields{"unavailable-sites": unavailableSites, "request-id": req.Id}).Warn("Wasn't able to contact all the requested sites")
	}
	mapResponses.UnavailableSites = unavailableSites
	return mapResponses, nil
}

// Sends an RPC carrying the compute request to a site. The
// response is then sent through a channel to the function
// waiting for the responses.
//
// req: The compute request to be sent to a site.
// site: An item from the SiteConnector map that contains the
//       site id as key and the ip and port of the site as the
//       value.
// ch: The channel where the response is sent to.
func (c *Coordinator) getResultFromSite(req *pb.MapRequest, site SiteConnector, ch chan ResultFromSite) {
	conn, err := c.Dial(site.ipPort, c.Conf.SiteConnCN)
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithCancel(context.Background())
	//ctx, cancel := context.WithTimeout(context.Background(), time.Second*10000)
	defer cancel()

	stream, err := client.Map(ctx)
	currentTime := time.Now().UnixNano()
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Start send to site connector")
	err = sendMapRequestStream(req, stream)
	currentTime = time.Now().UnixNano()
	checkErr(c, err)
	c.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End send to site connector")
	response, err := receiveMapResponseStream(stream)
	checkErr(c, err)

	// If site unavailable, update its available to false
	if utils.IsUnavailableError(err) {
		site.availableMux.Lock()
		site.available = false
		site.availableMux.Unlock()
		c.Log.WithFields(logrus.Fields{"site-id": site.id, "request-id": req.Id}).Warn("Site is unavailable.")
	} else {
		site.availableMux.Lock()
		site.available = true
		site.availableMux.Unlock()
	}

	// Send response to goroutine waiting for responses
	ch <- ResultFromSite{Response: response, Err: err, SiteId: site.id}
}

// Given a list of results from different sites, filter and
// return only the error responses from sites that were
// unavailable.
//
// results: A list of results from different sites.
func getUnavailableSites(results []ResultFromSite) []int64 {
	unavailableSites := []int64{}
	for _, result := range results {
		if utils.IsUnavailableError(result.Err) {
			unavailableSites = append(unavailableSites, result.SiteId)
		}
	}
	return unavailableSites
}

// Given a list of results from different sites, filter and
// return only the responses from sites that do not contain
// an error.
//
// results: A list of results from different sites.
func getSuccessfulResponses(results []ResultFromSite) pb.MapResponses {
	successfulResponses := pb.MapResponses{Responses: []*pb.MapResponse{}, UnavailableSites: []int64{}}
	for _, result := range results {
		if result.Err == nil {
			successfulResponses.Responses = append(successfulResponses.Responses, result.Response)
		}
	}
	return successfulResponses
}

// Receives a stream of bytes from the cloud algo
//
// stream: Stream containing the bytes to be received
func receiveMapRequestStream(stream pb.Coordinator_MapServer) (*pb.MapRequest, error) {
	recvBuf := []byte{}
	for {
	    chunk, err := stream.Recv()
	    if err == io.EOF {
	        break
	    }

	    if err != nil {
	        return nil, err
	    }

	    recvBuf = append(recvBuf, chunk.Chunk...)
	}

	req := &pb.MapRequest{}
	proto.Unmarshal(recvBuf, req)
	return req, nil
}

// Sends a stream of bytes to cloud algo
//
// results: List of map responses to turn into a bytes stream
// stream:  Grpc stream where the bytes are sent
func sendMapResponseStream(results *pb.MapResponses, stream pb.Coordinator_MapServer) error {
	sendBuf, _ := proto.Marshal(results)
	chunkSize := 64 * 1024
	for currByte := 0; currByte < len(sendBuf); currByte += chunkSize {
	    chunk := &pb.MapResponsesChunk{}
	    if currByte + chunkSize > len(sendBuf) {
	        chunk.Chunk = sendBuf[currByte:len(sendBuf)]
	    } else {
	        chunk.Chunk = sendBuf[currByte: currByte + chunkSize]
	    }
	    if err := stream.Send(chunk); err != nil {
	        return err
	    }
	}
	return nil
}

func sendMapRequestStream(req *pb.MapRequest, stream pb.SiteConnector_MapClient) error {
	sendBuf, err := proto.Marshal(req)
	chunkSize := 64 * 1024
	for currByte := 0; currByte < len(sendBuf); currByte += chunkSize {
	    chunk := &pb.MapRequestChunk{}
	    if currByte + chunkSize > len(sendBuf) {
	        chunk.Chunk = sendBuf[currByte:len(sendBuf)]
	    } else {
	        chunk.Chunk = sendBuf[currByte: currByte + chunkSize]
	    }

	    if err = stream.Send(chunk); err != nil {
	        return err
	    }
	}
	stream.CloseSend()
	return nil

}

func receiveMapResponseStream(stream pb.SiteConnector_MapClient) (*pb.MapResponse, error) {
	recvBuf := []byte{}
	for {
	    chunk, err := stream.Recv()
	    if err == io.EOF {
		break
	    }

	    if err != nil {
	        return nil, err
	    }

	    recvBuf = append(recvBuf, chunk.Chunk...)
	}

	req := &pb.MapResponse{}
	proto.Unmarshal(recvBuf, req)
	return req, nil

}
