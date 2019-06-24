package coordinator

import (
	"context"
	"github.com/sirupsen/logrus"
	"leap/Concurrent"
	pb "leap/ProtoBuf"
	"strconv"
)

// Registers a ste algorithm at a coordinator. This allows
// cloud algorithms to send compute requests to registered
// site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the site and algo id
//      of the algorithm to be registered.
func (c *Coordinator) RegisterSiteAlgo(ctx context.Context, req *pb.SiteRegReq) (*pb.SiteAlgoRegRes, error) {
	c.Log.WithFields(logrus.Fields{"site-id": req.SiteId, "algo-id": req.Req.AlgoId}).Info("Received registration request.")
	siteId := req.SiteId
	algoId := req.Req.AlgoId
	ipPort := req.SiteIpPort

	if c.SiteConnectors.Contains(algoId) {
		sitesWithAlgo := c.SiteConnectors.Get(algoId).(*Concurrent.Map)
		sitesWithAlgo.Set(siteId, ipPort)
	} else {
		c.SiteConnectors.Set(algoId, Concurrent.NewMap())
		sitesWithAlgo := c.SiteConnectors.Get(algoId).(*Concurrent.Map)
		sitesWithAlgo.Set(siteId, ipPort)
	}

	msg := "Algo " + strconv.Itoa(int(algoId)) + " registered successfully"
	response := pb.SiteAlgoRegRes{Success: true, Msg: msg}
	return &response, nil
}
