// The site connector grpc service that gets exposed to
// the coordinator.

package siteconnector

import (
	"context"
	pb "leap/proto"
)

// Verifies the selector and returns a success or error response
// to coordinator.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: selector verification request.
func (sc *SiteConnector) VerifySelector(ctx context.Context, req *pb.SelectorVerificationReq) (*pb.SelectorVerificationRes, error) {
	sc.Log.Info("Received request for verifying the selector.")
	conn, err := sc.Dial(sc.Conf.AlgoIpPort, sc.Conf.SiteAlgoCN)

	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	res, err := client.VerifySelector(context.Background(), req)

	if err != nil {
		sc.Log.Warn("Site Algo is unavailable.")
		return nil, err
	}

	return res, err
}
