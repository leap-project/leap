// The coordinator grpc service that gets exposed to the
// cloud algos.

package coordinator

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	pb "leap/proto"
	"leap/utils"
	"time"

	"github.com/sirupsen/logrus"
)

type ResultFromSite struct {
	Response *pb.MapResponse
	Err      error
	SiteId   int32
}

// Makes a remote procedure call to a site connector with a
// map request and returns the results of computing the map
// function on multiple sites.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Map request containing user defined functions.
func (c *Coordinator) Map(ctx context.Context, req *pb.MapRequest) (*pb.MapResponses, error) {
	c.PendingRequests.Set(req.Id, req.Id)
	if c.SiteConnectors.Length() == 0 {
		c.Log.WithFields(logrus.Fields{"request-id": req.Id}).Warn("No sites have been registered.")
		return nil, status.Error(codes.Unavailable, "There have been no sites registered.")
	}

	results, err := c.getResultsFromSites(req)

	return &results, err
}


// Makes a remote procedure call to a site connector asking
// it to return all available sites in the system.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Availability request
func (c *Coordinator) SitesAvailable(ctx context.Context, req *pb.SitesAvailableReq) (*pb.SitesAvailableRes, error) {
	c.Log.Info("Received request checking site availability")

	ch  := make(chan *pb.SiteAvailableRes)
	sitesLength := 0

	for item := range c.SiteConnectors.Iter() {
		siteConnec := item.Value.(SiteConnector)
		go c.isSiteAvailable(siteConnec, ch)
		sitesLength++
	}

	responses := make([]*pb.SiteAvailableRes, 0)
	for i := 0; i < sitesLength; i++ {
		select {
		case response := <-ch:
			responses = append(responses, response)
		}
	}
	return &pb.SitesAvailableRes{Responses: responses}, nil
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
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := client.Map(ctx, req)

	// If site unavailable, update its status to false
	if utils.IsUnavailableError(err) {
		site.statusMux.Lock()
		site.status = false
		site.statusMux.Unlock()
		c.Log.WithFields(logrus.Fields{"site-id": site.id, "request-id": req.Id}).Warn("Site is unavailable.")
	} else {
		site.statusMux.Lock()
		site.status = true
		site.statusMux.Unlock()
	}

	// Send response to goroutine waiting for responses
	ch <- ResultFromSite{Response: response, Err: err, SiteId: site.id}
}

// Given a list of results from different sites, filter and
// return only the error responses from sites that were
// unavailable.
//
// results: A list of results from different sites.
func getUnavailableSites(results []ResultFromSite) []int32 {
	unavailableSites := []int32{}
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
	successfulResponses := pb.MapResponses{Responses: []*pb.MapResponse{}, UnavailableSites: []int32{}}
	for _, result := range results {
		if result.Err == nil {
			successfulResponses.Responses = append(successfulResponses.Responses, result.Response)
		}
	}
	return successfulResponses
}

// Sends an RPC that checks whether a site is available.
//
// req: The site available request to be sent to a site.
// site: A site struct containing the id of a site.
// ch: The channel where the response is sent to.
func (c *Coordinator) isSiteAvailable(site SiteConnector, ch chan *pb.SiteAvailableRes)  {
	req := pb.SiteAvailableReq{SiteId: site.id}

	conn, err := c.Dial(site.ipPort, c.Conf.SiteConnCN)
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	_, err = client.SiteAvailable(ctx, &req)
	if err != nil {
		protoSite := pb.Site{SiteId: site.id, Available: false}
		res := pb.SiteAvailableRes{
			Site: &protoSite,
		}
		ch <- &res
	} else {
		protoSite := pb.Site{SiteId: site.id, Available: true}
		res := pb.SiteAvailableRes{
			Site: &protoSite,
		}
		ch <- &res
	}
}