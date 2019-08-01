package Tests

import (
	"context"
	"google.golang.org/grpc"
	"leap/Coordinator"
	"leap/Errors"
	pb "leap/ProtoBuf"
	"testing"
	"time"
)

func TestRegister(t *testing.T) {
	coordIpPort := "127.0.0.1:5000"
	coord := coordinator.NewCoordinator(coordinator.Config{IpPort: coordIpPort})
	go coord.Serve()
	time.Sleep(200 * time.Millisecond)

	request := pb.CloudAlgoRegReq{Id: 0, Description: "count", ProtoVersion: "proto3", AlgoIpPort: ""}
	conn, _ := grpc.Dial(coordIpPort, grpc.WithInsecure())
	client := pb.NewCoordinatorClient(conn)

	_, err := client.RegisterCloudAlgo(context.Background(), &request)
	if err == nil {
		t.Errorf("Expected an error, got: %s, want: %s.", err.Error(), Errors.NewSiteAlgoNotRegisteredError().Error())
	}

	//listOfSites := Concurrent.NewMap()
	//listOfSites.Set(0, "")
	//coord.SiteConnectors.Set(0, listOfSites)
	//t.Log(coord)
	//_, err = client.RegisterCloudAlgo(context.Background(), &request)
	//if err != nil {
	//	t.Errorf("Expected no error, got: %s, want: %s.", err.Error(), "nil")
	//}
}

func TestCompute(t *testing.T) {

}
