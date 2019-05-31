package main

import (
	"context"
	"errors"
	"fmt"
	"google.golang.org/grpc"
	pb "leap/ProtoBuf"
	"time"
)

/*
Service containing the API for interactions between the cloud
and a coordinator.
 */
type CloudCoordinatorService struct{}

/*

 */
func (s *CloudCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.CloudAlgoRegReq) (*pb.CloudAlgoRegRes, error) {
	return nil, nil
}

/*
Makes a remote procedure call to a site connector with a
query and returns the results of computing the query on
multiple site algorithms.

ctx: Carries value and cancellation signals across API
     boundaries.
req: Request created by algorithm in the cloud.
 */
func (s *CloudCoordinatorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponses, error) {
	fmt.Println("Coordinator: Compute request received")

	sites := SiteConnectors[req.AlgoId]
	if len(sites) == 0 {
		noSitesError := errors.New("There are no live sites for this algorithm")
		return &pb.ComputeResponses{}, noSitesError
	}

	var results pb.ComputeResponses
	for _, ipPort := range sites {
		conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
		checkErr(err)
		defer conn.Close()

		c := pb.NewCoordinatorConnectorClient(conn)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()

		localResponse, err := c.Compute(ctx, req)
		checkErr(err)
		results.Responses = append(results.Responses, localResponse)
	}

	return &results, nil
}