package siteconnector

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
)

// Invokes algorithm in site and returns the result of per-
// forming the algorithm on the given query to the coordinator.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Request created by algorithm in the cloud and issued
//      by coordinator.
func (sc *SiteConnector) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Info("Received compute request.")
	sc.PendingRequests.Set(req.Id, req.Id)
	conn, err := grpc.Dial(sc.Conf.AlgoIpPort, grpc.WithInsecure())

	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	res, err := client.Compute(context.Background(), req)

	if CustomErrors.IsUnavailableError(err) {
		sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Warn("Site Algo is unavailable.")
		checkErr(sc, err)
		return nil, CustomErrors.NewSiteUnavailableError()
	}

	checkErr(sc, err)
	return res, nil
}
