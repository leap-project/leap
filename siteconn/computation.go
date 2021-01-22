package siteconnector

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc"
	"google.golang.org/grpc/status"
	pb "leap/proto"
	"leap/utils"
)

// Invokes map function in site and returns the result of run-
// ning the function on the local data.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Map request containing user defined functions.
func (sc *SiteConnector) Map(ctx context.Context, req *pb.MapRequest) (*pb.MapResponse, error) {
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Info("Received map request.")
	sc.PendingRequests.Set(req.Id, req.Id)
	conn, err := sc.Dial(sc.Conf.AlgoIpPort, sc.Conf.SiteAlgoCN)

	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	maxSizeOption := grpc.MaxCallRecvMsgSize(32*10e10)
	res, err := client.Map(context.Background(), req, maxSizeOption)
	if utils.IsUnavailableError(err) {
		sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Warn("Site Algo is unavailable.")
		checkErr(sc, err)
		return nil, status.Error(codes.Unavailable, "Site algo is unavailable")
	} else if err != nil {
		sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Error(err)
		return nil, err
	}

	return res, err
}
