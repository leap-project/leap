package main

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
)

// Service containing the API for interactions between the site
// connector and the coordinator.
type CoordinatorConnectorService struct{}

// Invokes algorithm in site and returns the result of per-
// forming the algorithm on the given query to the coordinator.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Request created by algorithm in the cloud and issued
//      by coordinator.
func (s *CoordinatorConnectorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Info("Received compute request.")
	algoIpPort := siteConn.SiteAlgos.Get(req.AlgoId).(string)
	conn, err := grpc.Dial(algoIpPort, grpc.WithInsecure())

	checkErr(err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	res, err := client.Compute(context.Background(), req)

	if CustomErrors.IsUnavailableError(err) {
		log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Warn("Algo is unavailable.")
		checkErr(err)
		siteConn.SiteAlgos.Delete(req.AlgoId)
		return nil, CustomErrors.NewAlgoUnavailableError()
	}

	checkErr(err)
	return res, nil
}
