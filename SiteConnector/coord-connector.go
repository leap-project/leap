package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	pb "leap/ProtoBuf"
)

/*
Service containing the API for interactions between the site
connector and the coordinator.
 */
type CoordinatorConnectorService struct {}

/*
Invokes algorithm in site and returns the result of per-
forming the algorithm on the given query to the coordinator.

ctx: Carries value and cancellation signals across API
     boundaries.
req: Request created by algorithm in the cloud and issued
     by coordinator.
 */
func (s *CoordinatorConnectorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	fmt.Println("Site-Connector: Compute request received")

	algoIpPort := algos[req.AlgoId]
	conn, err := grpc.Dial(algoIpPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	fmt.Println(conn.GetState())
	res, err := client.Compute(context.Background(), req)
	checkErr(err)
	return res, nil
}