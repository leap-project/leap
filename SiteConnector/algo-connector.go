package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	pb "leap/ProtoBuf"
	"time"
)

/*
Service containing the API for interactions between the site
connector and the site algorithms.
 */
type AlgoConnectorService struct {}

func (s *AlgoConnectorService) RegisterAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	fmt.Println("Site-Connector: Registration request received")

	newRequest := pb.SiteRegReq{SiteId: siteId, SiteIpPort: config.ListenCoordinatorIpPort, Req: req}
	conn, err := grpc.Dial(config.CoordinatorIpPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	c := pb.NewSiteCoordinatorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	response, err := c.RegisterAlgo(ctx, &newRequest)
	if err == nil && response.Success {
		algos[req.AlgoId] = req.AlgoIpPort
	}
	checkErr(err)
	return response, err
}
