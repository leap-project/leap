package coordinator

import (
	"context"
	"github.com/sirupsen/logrus"
	pb "leap/ProtoBuf"
	"strconv"
)

// Registers a site at a coordinator. This allows cloud
// algorithms to send compute requests to registered site
// algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the site and algo id
//      of the algorithm to be registered.
func (c *Coordinator) RegisterSite(ctx context.Context, req *pb.SiteRegReq) (*pb.SiteRegRes, error) {
	c.Log.WithFields(logrus.Fields{"site-id": req.SiteId}).Info("Received registration request.")
	siteId := req.SiteId
	ipPort := req.SiteIpPort

	c.SiteConnectors.Set(siteId, ipPort)

	msg := "Site " + strconv.Itoa(int(siteId)) + " registered successfully"
	response := pb.SiteRegRes{Success: true, Msg: msg}
	return &response, nil
}
