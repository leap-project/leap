package main

import (
	"context"
	"github.com/sirupsen/logrus"
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
	log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Info("Received registration request.")
	newRequest := pb.SiteRegReq{SiteId: siteConn.Conf.SiteId, SiteIpPort: siteConn.Conf.ListenCoordinatorIpPort, Req: req}
	conn, err := grpc.Dial(siteConn.Conf.CoordinatorIpPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()

	c := pb.NewSiteCoordinatorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := c.RegisterAlgo(ctx, &newRequest)
	if CustomErrors.IsUnavailableError(err) {
		log.Warn("Coordinator is unavailable.")
		checkErr(err)
		return nil, CustomErrors.NewCoordinatorUnavailableError()
	}

	if err == nil && response.Success {
		siteConn.SiteAlgos.Set(req.AlgoId, req.AlgoIpPort)
	}
	checkErr(err)
	return response, err
}
