package main

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"leap/Concurrent"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
	"sync/atomic"
	"time"
)

// Service containing the API for interactions between the cloud
// and a coordinator.
type CloudCoordinatorService struct{}

type ErrorCounter struct {
	NumUnavailableSites int32
	NumUnavailableAlgos int32
}

type ResultFromSite struct {
	Err       error
	Response *pb.ComputeResponse
}

// Registers a cloud algorithm at a coordinator. This allows
// cloud algorithms to send compute requests to registered
// site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the algo id
//      of the algorithm to be registered.
func (s *CloudCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.CloudAlgoRegReq) (*pb.CloudAlgoRegRes, error) {
	log.WithFields(logrus.Fields{"algo-id": req.Id}).Info("Received registration request.")
	if !SiteConnectors.Contains(req.Id) {
		err := CustomErrors.NewSiteAlgoNotRegisteredError()
		log.WithFields(logrus.Fields{"algo-id": req.Id}).Warn(err.Error())
		return nil, err
	}

	CloudAlgos.Set(req.Id, req.AlgoIpPort)
	response := pb.CloudAlgoRegRes{Success: true, Msg: "Algorithm successfully registered."}
	log.WithFields(logrus.Fields{"algo-id": req.Id}).Info("Algo successfully registered.")
	return &response, nil
}

// Makes a remote procedure call to a site connector with a
// query and returns the results of computing the query on
// multiple site algorithms.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Request created by algorithm in the cloud.
func (s *CloudCoordinatorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponses, error) {
	log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Info("Received compute request.")
	res, err := isRegistrationError(*req)
	if err != nil {
		log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Warn(err.Error())
		return res, err
	}

	sites := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
	results, err := getResultsFromSites(req, sites)

	if err != nil {
		return &results, err
	}

	return &results, nil
}

// Spawns a goroutine for each site that can support the
// algorithm in the request. The responses are then received
// through a channel and append to the results. The results
// are then returned to calling algorithm in the cloud.
//
// req: The compute request to be sent to each site.
// sites: The sites that the requests are going to be sent to.
func getResultsFromSites(req *pb.ComputeRequest, sites *Concurrent.Map) (pb.ComputeResponses, error) {
	var responses pb.ComputeResponses
	c := make(chan ResultFromSite)

	sitesLength := int32(0)
	counters := ErrorCounter{NumUnavailableSites: 0, NumUnavailableAlgos: 0}

	// Asynchronously send compute request to each site.
	for item := range sites.Iter() {
		go getResultFromSite(req, item, &counters, c)
		sitesLength++
	}

	// Append the responses to the asynchronous requests
	for i := int32(0); i < sitesLength; i++ {
		select {
			case response := <-c:
				if response.Err == nil {
					responses.Responses = append(responses.Responses, response.Response)
				}
		}
	}

	// Determine type of error if there is any
	if counters.NumUnavailableSites == sitesLength {
		return responses, CustomErrors.NewSiteUnavailableError()
	} else if counters.NumUnavailableAlgos == sitesLength {
		return responses, CustomErrors.NewAlgoUnavailableError()
	}

	return responses, nil
}

// Sends an RPC carrying the compute request to a site. The
// response is then sent through a channel to the function
// waiting for the responses. If the site or algo is unavailable,
// it is removed from the map of available algos.
//
// req: The compute request to be sent to a site.
// item: An item from the SiteConnector map that contains the
//       site id as key and the ip and port of the site as the
//       value.
// counters: A counter for the amount of requests that fail
//           because the algorithm is unavailable.
// ch: The channel where the response is sent to.
func getResultFromSite(req *pb.ComputeRequest, item Concurrent.Item, counters *ErrorCounter, ch chan ResultFromSite) {
	siteId := item.Key
	ipPort := item.Value.(string)

	conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	c := pb.NewCoordinatorConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := c.Compute(ctx, req)

	// If error, increment appropriate counter and delete unavailable sites and algos
	if CustomErrors.IsAlgoUnavailableError(err) {
		atomic.AddInt32(&counters.NumUnavailableAlgos, 1)
		sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
		sitesWithAlgo.Delete(siteId)
		log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Warn("Algo is unavailable.")
		checkErr(err)
	} else if CustomErrors.IsUnavailableError(err) {
		atomic.AddInt32(&counters.NumUnavailableSites, 1)
		sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
		sitesWithAlgo.Delete(siteId)
		log.WithFields(logrus.Fields{"site-id": siteId}).Warn("Site is unavailable.")
		checkErr(err)
	}

	// Send response to goroutine waiting for responses
	ch <- ResultFromSite{Response: response, Err: err}
}

// This function checks the number of sites that have the
// algorithm requested in the id, and if there are any
// cloud algos with the requested id. If there are no sites
// with the requested id, a SiteAlgoNotRegisteredError is
// returned. If there are no cloud algos with the requested
// id, return a CloudAlgoNotRegisteredError.
//
// req: A request that has the id of the algorithm being
//      requested.
func isRegistrationError(req pb.ComputeRequest) (*pb.ComputeResponses, error) {
	containsCloudAlgo := CloudAlgos.Contains(req.AlgoId)
	containsSiteAlgo := containsSiteAlgo(req.AlgoId)
	if !containsSiteAlgo {
		return &pb.ComputeResponses{}, CustomErrors.NewSiteAlgoNotRegisteredError()
	} else if !containsCloudAlgo {
		return &pb.ComputeResponses{}, CustomErrors.NewCloudAlgoNotRegisteredError()
	} else {
		return &pb.ComputeResponses{}, nil
	}
}

// Returns true if there are any site algos with the id given
// as a parameter. Return false otherwise.
//
// algoId: The id of a site algo.
func containsSiteAlgo(algoId int32) bool {
	if !SiteConnectors.Contains(algoId) {
		return false
	}

	ips := SiteConnectors.Get(algoId).(*Concurrent.Map)
	if ips.Length() == 0 {
		return false
	} else {
		return true
	}
}
