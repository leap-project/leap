package coordinator

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"leap/Concurrent"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
	"time"
)

type ErrorCounter struct {
	NumUnavailableSites int32
	NumUnavailableAlgos int32
}

type ResultFromSite struct {
	Err       error
	Response *pb.ComputeResponse
}

// Makes a remote procedure call to a site connector with a
// query and returns the results of computing the query on
// multiple site algorithms.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Request created by algorithm in the cloud.
func (c *Coordinator) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponses, error) {
	c.IdMux.Lock()
	id := c.NextId
	c.NextId = c.NextId + 1
	c.IdMux.Unlock()

	c.PendingRequests.Set(id, id)
	c.Log.WithFields(logrus.Fields{"request-id": id}).Info("Received compute request.")

	req.Id = id
	results, err := c.getResultsFromSites(req)

	if err != nil {
		return &results, err
	}

	return &results, nil
}

// Spawns a goroutine for each site that can support the
// algorithm in the request. The responses are then received
// through a channel and appended to the results. The results
// are returned to the calling algorithm in the cloud.
//
// req: The compute request to be sent to each site.
func (c *Coordinator) getResultsFromSites(req *pb.ComputeRequest) (pb.ComputeResponses, error) {
	var responses pb.ComputeResponses
	ch := make(chan ResultFromSite)

	sitesLength := 0

	// Asynchronously send compute request to each site.
	for item := range c.SiteConnectors.Iter() {
		go c.getResultFromSite(req, item, ch)
		sitesLength++
	}

	// Append the responses to the asynchronous requests
	for i := 0; i < sitesLength; i++ {
		select {
			case response := <-ch:
				if response.Err == nil {
					responses.Responses = append(responses.Responses, response.Response)
				}
		}
	}

	// Determine if there were unavailable sites
	if len(responses.Responses) == sitesLength {
		return responses, CustomErrors.NewSiteUnavailableError()
	}

	return responses, nil
}

// Sends an RPC carrying the compute request to a site. The
// response is then sent through a channel to the function
// waiting for the responses. If the site is unavailable,
// it is removed from the map of available algos.
//
// req: The compute request to be sent to a site.
// site: An item from the SiteConnector map that contains the
//       site id as key and the ip and port of the site as the
//       value.
// ch: The channel where the response is sent to.
func (c *Coordinator) getResultFromSite(req *pb.ComputeRequest, site Concurrent.Item, ch chan ResultFromSite) {
	siteId := site.Key
	ipPort := site.Value.(string)

	conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := client.Compute(ctx, req)

	// If error, increment appropriate counter and delete unavailable sites and algos
	if CustomErrors.IsUnavailableError(err) {
		c.SiteConnectors.Delete(siteId)
		c.Log.WithFields(logrus.Fields{"site-id": siteId}).Warn("Site is unavailable.")
		checkErr(c, err)
	}
	// Send response to goroutine waiting for responses
	ch <- ResultFromSite{Response: response, Err: err}
}