package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"leap/Concurrent"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
	"time"
)

// Service containing the API for interactions between the cloud
// and a coordinator.
type CloudCoordinatorService struct{}

// Registers a cloud algorithm at a coordinator. This allows
// cloud algorithms to send compute requests to registered
// site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the algo id
//      of the algorithm to be registered.
func (s *CloudCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.CloudAlgoRegReq) (*pb.CloudAlgoRegRes, error) {
	if SiteConnectors.Contains(req.Id) {
		sites := SiteConnectors.Get(req.Id).(*Concurrent.Map)
		if  sites.Length() == 0 {
			return nil, CustomErrors.NewSiteAlgoNotRegisteredError()
		}
		CloudAlgos.Set(req.Id, req.AlgoIpPort)
		response := pb.CloudAlgoRegRes{Success: true, Msg: "Algorithm successfully registered."}
		return &response, nil
	} else {
		return nil, CustomErrors.NewSiteAlgoNotRegisteredError()
	}
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

	if !SiteConnectors.Contains(req.AlgoId) {
		return nil, CustomErrors.NewSiteAlgoNotRegisteredError()
	}

	sites := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
	res, err := selectRegistrationError(*req)
	if err != nil {
		return res, err
	}

	results, err := getResultsFromSites(req, sites)

	if err != nil {
		return &results, err
	}

	return &results, nil
}

// Sends a ComputeRequest to all the sites that have the algo
// specified in the request. The results are then added to a
// ComputeResponses struct, which is returned to the caller.
// If all contacted sites are unavailable, returns an error
// indicating that there are no sites live that support the re-
// quested algorithm.
//
// req: The compute request to be sent to each site.
// sites: The sites that the requests are going to be sent to.
func getResultsFromSites(req *pb.ComputeRequest, sites *Concurrent.Map) (pb.ComputeResponses, error) {
	var results pb.ComputeResponses
	numUnavailableSites := 0
	numUnavailableAlgos := 0
	sitesLength := 0

	for item := range sites.Iter() {
		key := item.Key
		ipPort := item.Value.(string)
		response, err := getResultFromSite(req, ipPort)
		checkErr(err)

		if CustomErrors.IsAlgoUnavailableError(err) {
			numUnavailableAlgos++
			sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
			sitesWithAlgo.Delete(key)
		} else if CustomErrors.IsUnavailableError(err) {
			numUnavailableSites++
			sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
			sitesWithAlgo.Delete(key)
		} else {
			results.Responses = append(results.Responses, response)
		}

		sitesLength++
	}

	if numUnavailableSites == sitesLength {
		return results, CustomErrors.NewSiteUnavailableError()
	} else if numUnavailableAlgos == sitesLength {
		return results, CustomErrors.NewAlgoUnavailableError()
	}

	return results, nil
}

// Sends an RPC carrying the compute request to the site with
// the ip and port specified in the parameters. The response
// to the RPC is returned.
//
// req: The compute request to be sent to a site.
// ipPort: The ip and port of the site hosting the desired
//         algorithm.
func getResultFromSite(req *pb.ComputeRequest, ipPort string) (*pb.ComputeResponse, error) {
	conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	c := pb.NewCoordinatorConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	localResponse, err := c.Compute(ctx, req)

	return localResponse, err
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
func selectRegistrationError(req pb.ComputeRequest) (*pb.ComputeResponses, error) {
	sitesWithAlgo := SiteConnectors.Get(req.AlgoId).(*Concurrent.Map)
	contains := CloudAlgos.Contains(req.AlgoId)

	if sitesWithAlgo.Length() == 0 {
		return &pb.ComputeResponses{}, CustomErrors.NewSiteAlgoNotRegisteredError()
	} else if !contains {
		return &pb.ComputeResponses{}, CustomErrors.NewCloudAlgoNotRegisteredError()
	} else {
		return &pb.ComputeResponses{}, nil
	}
}
