package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"google.golang.org/grpc"
	"io/ioutil"
	pb "leap/ProtoBuf"
	"net"
	"os"
)

type AlgoId int32

type Config struct {
	ListenCoordinatorIpPort string
	ListenAlgosIpPort string
	Coordinator string

}

type AlgoConnectorService struct {}
type CoordinatorConnectorService struct {}

var (
	config Config
	algos = make(map[AlgoId]string)
)

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

	CoordinatorIpPortPtr := flag.String("cip", config.ListenCoordinatorIpPort, "The ip and port to listen for coordinators")
	AlgosIpPortPtr := flag.String("aip", config.ListenAlgosIpPort, "The ip and port to listen for site algorithms")
	flag.Parse()

	config.ListenAlgosIpPort = *CoordinatorIpPortPtr
	config.ListenCoordinatorIpPort = *AlgosIpPortPtr
	algos[0] = "127.0.0.1:60000"
}

/*
Invokes algorithm in site and returns the result of per-
forming the algorithm on the given query to the coordinator.

ctx: Carries value and cancellation signals across API
     boundaries.
req: Request created by algorithm in the cloud and issued
     by coordinator.
 */
func (s *CoordinatorConnectorService) Compute(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	fmt.Println("Site-Connector: Compute request received")
	ipPort := algos[AlgoId(req.AlgoId)]
	conn, err := grpc.Dial(ipPort, grpc.WithInsecure())
	checkErr(err)
	defer conn.Close()
	client := pb.NewSiteAlgoClient(conn)
	res, err := client.Compute(context.Background(), req)
	checkErr(err)
	return res, nil
}

/*
Serves RPC calls from site algorithms.

No args.
*/
func ListenAlgos() {
	listener, err := net.Listen("tcp", config.ListenAlgosIpPort)
	fmt.Println("Site-Connector: Listening for site algos at", config.ListenAlgosIpPort)
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterAlgoConnectorServer(s, &AlgoConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Serves RPC calls from coordinator.

No args.
*/
func ListenCoordinator() {
	listener, err := net.Listen("tcp", config.ListenCoordinatorIpPort)
	fmt.Println("Site-Connector: Listening for coordinator at", config.ListenCoordinatorIpPort)
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterCoordinatorConnectorServer(s, &CoordinatorConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Helper to log errors in a site connector.

err: Error returned by a function that should be checked
     if nil or not.
*/
func checkErr(err error) {
	if err != nil {
		fmt.Println("Site Connector:", err.Error())
	}
}