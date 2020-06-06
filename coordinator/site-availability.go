package coordinator

import (
	"context"
	pb "leap/proto"
	"time"
)

// Makes a remote procedure call to a site connector asking
// it to return whether it is available.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Availability request
func (c *Coordinator) SitesAvailable(ctx context.Context, req *pb.SitesAvailableReq) (*pb.SitesAvailableRes, error) {
	c.Log.Info("Received request checking site availability.")

	ch := make(chan *pb.SiteAvailableRes)
	sitesLength := 0

	for item := range c.SiteConnectors.Iter() {
		siteConnec := item.Value.(SiteConnector)
		go c.isSiteAvailable(siteConnec, ch)
		sitesLength++
	}

	responses := make([]*pb.SiteAvailableRes, 0)
	for i := 0; i < sitesLength; i++ {
		select {
		case response := <-ch:
			responses = append(responses, response)
		}
	}
	return &pb.SitesAvailableRes{Responses: responses}, nil
}

// Sends an RPC that checks whether a site is available.
//
// req: The site available request to be sent to a site.
// site: A site struct containing the id of a site.
// ch: The channel where the response is sent to.
func (c *Coordinator) isSiteAvailable(site SiteConnector, ch chan *pb.SiteAvailableRes) {
	req := pb.SiteAvailableReq{SiteId: site.id}

	conn, err := c.Dial(site.ipPort, c.Conf.SiteConnCN)
	checkErr(c, err)
	defer conn.Close()

	client := pb.NewSiteConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	res, err := client.SiteAvailable(ctx, &req)
	if err != nil {
		protoSite := pb.Site{SiteId: site.id, Available: false}
		res := pb.SiteAvailableRes{
			Site: &protoSite,
		}
		ch <- &res
	} else {
		protoSite := pb.Site{SiteId: site.id, Available: res.Site.Available}
		res := pb.SiteAvailableRes{
			Site: &protoSite,
		}
		ch <- &res
	}
}
