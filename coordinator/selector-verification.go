package coordinator

import (
	"context"
	pb "leap/proto"
	"time"
)

// Makes a RPC to a site connector asking it to verify
// the selector
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Selector verification request
func (c *Coordinator) VerifySelector(ctx context.Context, req *pb.SelectorVerificationsReq) (*pb.SelectorVerificationsRes, error) {
	c.Log.Info("Received request to verify selector.")

	ch := make(chan *pb.SelectorVerificationRes)
	sitesLength := 0

	for item := range c.SiteConnectors.Iter() {
		siteConnec := item.Value.(SiteConnector)
		go c.verifySelector(req, siteConnec, ch)
		sitesLength++
	}

	results := make([]*pb.SelectorVerificationRes, 0)
	for i := 0; i < sitesLength; i++ {
		select {
		case response := <-ch:
			results = append(results, response)
		}
	}
	return &pb.SelectorVerificationsRes{Responses: results}, nil

}

// Sends an RPC that verifies the selector
//
// req: The verification request to be sent to a site.
// site: A site struct containing the id of a site.
// ch: The channel where the response is sent to.
func (c *Coordinator) verifySelector(reqs *pb.SelectorVerificationsReq, site SiteConnector, ch chan *pb.SelectorVerificationRes) {
	req := pb.SelectorVerificationReq{SiteId: site.id, Selector: reqs.GetSelector(), IsSelectorString: reqs.IsSelectorString}

	conn, err := c.Dial(site.ipPort, c.Conf.SiteConnCN)
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	res, err := client.VerifySelector(ctx, &req)

	if err != nil {
		res := pb.SelectorVerificationRes{
			SiteId:  site.id,
			Success: false,
			Error:   err.Error(),
		}
		ch <- &res
	} else {
		ch <- res
	}

}
