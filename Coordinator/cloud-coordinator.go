package main

import (
	"context"
	"fmt"
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
	if !SiteConnectors.Contains(req.Id) {
		return nil, CustomErrors.NewSiteAlgoNotRegisteredError()
	}

	CloudAlgos.Set(req.Id, req.AlgoIpPort)
	response := pb.CloudAlgoRegRes{Success: true, Msg: "Algorithm successfully registered."}
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
	fmt.Println("Coordinator: Compute request received")
	res, err := isRegistrationError(*req)
	if err != nil {
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
	key := item.Key
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
		sitesWithAlgo.Delete(key)
	} else if CustomErrors.IsUnavailableError(err) {
		atomic.AddInt32(&counters.NumUnavailableSites, 1)
		sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
		sitesWithAlgo.Delete(key)
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
	contains := CloudAlgos.Contains(req.AlgoId)

	if !SiteConnectors.Contains(req.AlgoId) {
		return &pb.ComputeResponses{}, CustomErrors.NewSiteAlgoNotRegisteredError()
	} else if !contains {
		return &pb.ComputeResponses{}, CustomErrors.NewCloudAlgoNotRegisteredError()
	} else {
		return &pb.ComputeResponses{}, nil
	}
}
