package coordinator

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"leap/Errors"
	pb "leap/ProtoBuf"
	"time"

	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

type ResultFromSite struct {
	Response    *pb.MapResponse
	Err         error
	SiteId      int32
}

// Makes a remote procedure call to a site connector with a
// query and returns the results of computing the query on
// multiple site algorithms.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Request created by algorithm in the cloud.
func (c *Coordinator) Map(ctx context.Context, req *pb.MapRequest) (*pb.MapResponses, error) {
	c.PendingRequests.Set(req.Id, req.Id)
	c.Log.WithFields(logrus.Fields{"request-id": req.Id}).Info("Received map request.")
	if c.SiteConnectors.Length() == 0 {
		c.Log.Warn("No sites have been registered.")
		return nil, status.Error(codes.Unavailable, "There have been no sites registered.")
	}

	results, err := c.getResultsFromSites(req)

	return &results, err
}

// Spawns a goroutine for each site that can support the
// algorithm in the request. The responses are then received
// through a channel and appended to the results. The results
// are returned to the calling algorithm in the cloud.
//
// req: The compute request to be sent to each site.
func (c *Coordinator) getResultsFromSites(req *pb.MapRequest) (pb.MapResponses, error) {
	ch := make(chan ResultFromSite)

	sitesLength := 0

	// Asynchronously send compute request to each site.
	for item := range c.SiteConnectors.Iter() {
		site := item.Value.(SiteConnector)
			go c.getResultFromSite(req, site, ch)
			sitesLength++
	}

	// Append the responses to the asynchronous requests
	results := []ResultFromSite{}
	for i := 0; i < sitesLength; i++ {
		select {
		case response := <-ch:
			results = append(results, response)
		}
	}

	unavailableSites := getUnavailableSites(results)
	mapResponses := getSuccessfulResponses(results)
	// Determine if there were unavailable sites
	if len(unavailableSites) == sitesLength {
		c.Log.WithFields(logrus.Fields{"unavailable-sites": unavailableSites}).Error("Wasn't able to contact any of the registered sites")
		return mapResponses, status.Error(codes.Unavailable, "Wasn't able to contact any of the registered sites")
	} else if len(unavailableSites) > 0 {
		c.Log.WithFields(logrus.Fields{"unavailable-sites": unavailableSites}).Warn("Wasn't able to contact all the requested sites")
	}
	mapResponses.UnavailableSites = unavailableSites
	return mapResponses, nil
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
func (c *Coordinator) getResultFromSite(req *pb.MapRequest, site SiteConnector, ch chan ResultFromSite) {
	conn, err := grpc.Dial(site.ipPort, grpc.WithInsecure())
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := client.Map(ctx, req)

	// If site unavailable, update its status to false
	if Errors.IsUnavailableError(err) {
		site.statusMux.Lock()
		site.status = false
		site.statusMux.Unlock()
		c.Log.WithFields(logrus.Fields{"site-id": site.id}).Warn("Site is unavailable.")
		checkErr(c, err)
	} else {
		site.statusMux.Lock()
		site.status = true
		site.statusMux.Unlock()
	}
	// Send response to goroutine waiting for responses
	ch <- ResultFromSite{Response: response, Err: err, SiteId: site.id}
}

func getUnavailableSites(results []ResultFromSite) []int32 {
	unavailableSites := []int32{}
	for _, result := range results {
		if Errors.IsUnavailableError(result.Err) {
			unavailableSites = append(unavailableSites, result.SiteId)
		}
	}
	return unavailableSites
}

func getSuccessfulResponses(results []ResultFromSite) pb.MapResponses {
	successfulResponses := pb.MapResponses{Responses: []*pb.MapResponse{}, UnavailableSites: []int32{}}
	for _, result := range results {
		if result.Err == nil {
			successfulResponses.Responses = append(successfulResponses.Responses, result.Response)
		}
	}
	return successfulResponses
}

// TODO: Check site connector is unavailable
// Scenario: Coordinator pings site. Site doesn't respond (but is not actually down)
//           so site is removed from live sites. Site was not actually down, so it
//			 doesn't register again. Coordinator doesn't know site conn is available.
