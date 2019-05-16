package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"google.golang.org/grpc"
	"io/ioutil"
	pb "leap/protoBuf"
	"net"
	"os"
	"time"
)

var (
	config Config
)

type Message struct {
	msg string
}

type Config struct {
	IpPort string
}

type CloudCoordinatorService struct{}
type SiteCoordinatorService struct{}


func (s *SiteCoordinatorService) RegisterSite(ctx context.Context, req *pb.SiteRegReq) (*pb.SiteRegRes, error) {
 return nil, nil
}

func (s *SiteCoordinatorService) RegisterSiteAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	return nil, nil
}

func (s *CloudCoordinatorService) RegisterCloudAlgo(ctx context.Context, req *pb.CloudAlgoRegReq) (*pb.CloudAlgoRegRes, error) {
	return nil, nil
}

/*
Makes a remote procedure call to a site connector with a
query and returns the result of computing the query on a
site algorithm

ctx: Carries value and cancellation signals across API
     boundaries
req: Query created by algorithm in the cloud
 */
func (s *CloudCoordinatorService) Count(ctx context.Context, req *pb.Query) (*pb.QueryResponse, error) {
	conn, err := grpc.Dial("127.0.0.1:9000", grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()
	c := pb.NewCoordinatorConnectorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	res, err := c.Count(ctx, req)
	checkErr(err)
	return res, nil
}


/*
Serves RPC calls from sites

listener: A network listener at the ip and port specified by the config
*/
func ListenSites(listener net.Listener) {
	s := grpc.NewServer()
	pb.RegisterSiteCoordinatorServer(s, &SiteCoordinatorService{})
	err := s.Serve(listener)
	checkErr(err)
}

/*
Serves RPC calls from cloud algorithms

listener: A network listener at the ip and port specified by the config
*/
func ListenCloud(listener net.Listener) {
	s := grpc.NewServer()
	pb.RegisterCloudCoordinatorServer(s, &CloudCoordinatorService{})
	err := s.Serve(listener)
	checkErr(err)
}

/*
Parses user flags and creates config using the given flags.
If a flag is absent, use the default flag given in the
config.json file.

No args
 */
func InitializeConfig() {
	jsonFile, err := os.Open("config.json")
	checkErr(err)
	defer jsonFile.Close()
	jsonBytes, err := ioutil.ReadAll(jsonFile)
	checkErr(err)

	err = json.Unmarshal(jsonBytes, &config)
	checkErr(err)

	IpPortPtr := flag.String("ip", config.IpPort, "The ip and port the coordinator is listening on")
	flag.Parse()

	config.IpPort = *IpPortPtr
}


/*
Helper to log errors in the coordinator

err: Error returned by a function that should be checked
     if nil or not.
*/
func checkErr(err error) {
	if err != nil {
		fmt.Println("Coordinator:", err.Error())
	}
}
