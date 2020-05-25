// The site connector grpc service that gets exposed to
// the coordinator.

package siteconnector

import (
	"context"
	pb "leap/proto"
)

// Checks whether the site algo is running and return response
// to coordinator.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Availability request.
func (sc *SiteConnector) SiteAvailable(ctx context.Context, req *pb.SiteAvailableReq) (*pb.SiteAvailableRes, error) {
	sc.Log.Info("Received request checking for site availability.")
	conn, err := sc.Dial(sc.Conf.AlgoIpPort, sc.Conf.SiteAlgoCN)

	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	_, err = client.SiteAvailable(context.Background(), req)

	if err != nil {
		site := pb.Site{SiteId: sc.Conf.SiteId, Available: false}
		return &pb.SiteAvailableRes{Site: &site}, nil
	} else {
		site := pb.Site{SiteId: sc.Conf.SiteId, Available: true}
		return &pb.SiteAvailableRes{Site: &site}, nil
	}
}
