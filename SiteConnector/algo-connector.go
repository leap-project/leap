package siteconnector

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"leap/CustomErrors"
	pb "leap/ProtoBuf"
	"time"
)

// Sends a registration request from a site algo to the
// coordinator. This allows  cloud algorithms to send compute
// requests to registered site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the site and algo id
//      of the algorithm to be registered.
func (sc *SiteConnector) RegisterSiteAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	sc.Log.WithFields(logrus.Fields{"algo-id": req.AlgoId}).Info("Received registration request.")
	newRequest := pb.SiteRegReq{SiteId: sc.Conf.SiteId, SiteIpPort: sc.Conf.IpPort, Req: req}
	conn, err := grpc.Dial(sc.Conf.CoordinatorIpPort, grpc.WithInsecure())
	checkErr(sc, err)
	defer conn.Close()

	c := pb.NewCoordinatorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	response, err := c.RegisterSiteAlgo(ctx, &newRequest)
	if CustomErrors.IsUnavailableError(err) {
		sc.Log.Warn("Coordinator is unavailable.")
		checkErr(sc, err)
		return nil, CustomErrors.NewCoordinatorUnavailableError()
	}

	if err == nil && response.Success {
		sc.SiteAlgos.Set(req.AlgoId, req.AlgoIpPort)
	}
	checkErr(sc, err)
	return response, err
}
