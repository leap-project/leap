package main

import (
	"context"
	"errors"
	"fmt"
	"google.golang.org/grpc"
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
		noSitesError := errors.New("There are no sites with the algorithm id you want to register.")
		response := pb.CloudAlgoRegRes{Success: false, Msg: "There are no sites with the algorithm id you want to register."}
		return &response, noSitesError
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

	res, err := checkErrorsInRequest(*req)
	if err != nil {
		fmt.Println("ERRORRR")
		fmt.Println(*req)
		return res, err
	}

	var results pb.ComputeResponses
	for _, ipPort := range sites {
		conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
		checkErr(err)
		defer conn.Close()

		c := pb.NewCoordinatorConnectorClient(conn)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second * 5)
		defer cancel()

		localResponse, err := c.Compute(ctx, req)
		checkErr(err)
		results.Responses = append(results.Responses, localResponse)
	}

	return &results, nil
}

func checkErrorsInRequest(req pb.ComputeRequest) (*pb.ComputeResponses, error) {
	sites := SiteConnectors[req.AlgoId]
	_, contains := CloudAlgos[req.AlgoId]

	if len(sites) == 0 {
		noSitesError := errors.New("There are no live sites for this algorithm")
		return &pb.ComputeResponses{}, noSitesError
	} else if !contains {
		registrationError := errors.New("The cloud algo from the request is not registered.")
		return  &pb.ComputeResponses{}, registrationError
	} else {
		return &pb.ComputeResponses{}, nil
	}
}