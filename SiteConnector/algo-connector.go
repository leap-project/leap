package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
	"time"
)

// Service containing the API for interactions between the site
// connector and the site algorithms.
type AlgoConnectorService struct{}

// Sends a registration request from a site algo to the
// coordinator. This allows  cloud algorithms to send compute
// requests to registered site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the site and algo id
//      of the algorithm to be registered.
func (s *AlgoConnectorService) RegisterAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	fmt.Println("Site-Connector: Registration request received")

	newRequest := pb.SiteRegReq{SiteId: config.SiteId, SiteIpPort: config.ListenCoordinatorIpPort, Req: req}
	conn, err := grpc.Dial(config.CoordinatorIpPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	c := pb.NewSiteCoordinatorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := c.RegisterAlgo(ctx, &newRequest)
	if CustomErrors.IsUnavailableError(err) {
		return nil, CustomErrors.NewCoordinatorUnavailableError()
	}
	if err == nil && response.Success {
		SiteAlgos[req.AlgoId] = req.AlgoIpPort
	}
	checkErr(err)
	return response, err
}
