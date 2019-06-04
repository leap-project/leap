package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
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
	sites := SiteConnectors[req.Id]
	if len(sites) == 0 {
		response := pb.CloudAlgoRegRes{Success: false, Msg: "There are no sites with the algorithm id you want to register."}
		return &response, CustomErrors.NewSiteAlgoNotRegisteredError()
	}
	CloudAlgos[req.Id] = req.AlgoIpPort
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
	sites := SiteConnectors[req.AlgoId]

	res, err := selectRegistrationError(*req)
	if err != nil {
		return res, err
	}

	results := getResultsFromSites(req, sites)

	if len(results.Responses) == 0 {
		return &results, CustomErrors.NewSiteUnavailableError()
	}

	return &results, nil
}

// Sends a ComputeRequest to all the sites that have the algo
// specified in the request. The results are then added to a
// ComputeResponses struct, which is returned to the caller.
//
// req: The compute request to be sent to each site.
// sites: The sites that the requests are going to be sent to.
func getResultsFromSites(req *pb.ComputeRequest, sites map[int32]string) pb.ComputeResponses {
	var results pb.ComputeResponses

	for key, ipPort := range sites {
		conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
		checkErr(err)
		defer conn.Close()

		c := pb.NewCoordinatorConnectorClient(conn)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second * 5)
		defer cancel()

		localResponse, err := c.Compute(ctx, req)
		checkErr(err)
		if CustomErrors.IsSiteUnavailableError(err) {
			delete(SiteConnectors[req.AlgoId], key)
		} else {
			results.Responses = append(results.Responses, localResponse)
		}
	}
	return results
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
	sites := SiteConnectors[req.AlgoId]
	_, contains := CloudAlgos[req.AlgoId]

	if len(sites) == 0 {
		return &pb.ComputeResponses{}, CustomErrors.NewSiteAlgoNotRegisteredError()
	} else if !contains {
		return  &pb.ComputeResponses{}, CustomErrors.NewCloudAlgoNotRegisteredError()
	} else {
		return &pb.ComputeResponses{}, nil
	}
}