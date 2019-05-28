package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	pb "leap/ProtoBuf"
	"time"
)

type AlgoId int32
type CloudCoordinatorService struct{}

func (s *CloudCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.CloudAlgoRegReq) (*pb.CloudAlgoRegRes, error) {
	return nil, nil
}

/*
Makes a remote procedure call to a site connector with a
query and returns the result of computing the query on a
site algorithm.

ctx: Carries value and cancellation signals across API
     boundaries.
req: Request created by algorithm in the cloud.
 */
func (s *CloudCoordinatorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponses, error) {
	fmt.Println("Coordinator: Compute request received")
	sites := SiteConnectors[AlgoId(req.AlgoId)]
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