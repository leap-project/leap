package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"google.golang.org/grpc"
	"io/ioutil"
	pb "leap/ProtoBuf"
	"net"
	"os"
)

var (
	// Initial config
	config Config
	// IP and port of VM with algo given as key
	CloudAlgos = make(map[AlgoId]string)
	// IP's and ports of sites hosting algo given as key
	SiteConnectors = make(map[AlgoId]map[SiteId]string)
)

/*
The id of a site.
 */
type SiteId int32

/*
The id of an algorithm.
 */
type AlgoId int32


/*
A struct that holds the ip and port that the coordinator
listens for requests from algorithms in the cloud, and the
ip and port it listen for requests from algorithms in dis-
tributed sites.
 */
type Config struct {
	ListenCloudIpPort string
	ListenSiteIpPort  string
}

/*
Parses user flags and creates config using the given flags.
If a flag is absent, use the default flag given in the
config.json file.

No args.
 */
func InitializeCoordinator() {
	jsonFile, err := os.Open("config.json")
	checkErr(err)
	defer jsonFile.Close()
	jsonBytes, err := ioutil.ReadAll(jsonFile)
	checkErr(err)

	err = json.Unmarshal(jsonBytes, &config)
	checkErr(err)

	CloudIpPortPtr := flag.String("cip", config.ListenCloudIpPort, "The ip and port the coordinator is listening for cloud connections")
	SiteIpPortPtr := flag.String("sip", config.ListenSiteIpPort, "The ip and port the coordinator is listening for site connections")
	flag.Parse()

	config.ListenCloudIpPort = *CloudIpPortPtr
	config.ListenSiteIpPort = *SiteIpPortPtr
	SiteConnectors[0] = make(map[SiteId]string)
	SiteConnectors[0][0] = "127.0.0.1:50003"
}

/*
Creates a listener, registers the grpc server for coordinating
algorithms hosted in the cloud, and serves requests that arrive
at the listener.

No args.
*/
func ServeCloud() {
	listener, err := net.Listen("tcp", config.ListenCloudIpPort)
	checkErr(err)
	fmt.Println("Coordinator: Listening for cloud algos at", config.ListenCloudIpPort)
	s := grpc.NewServer()
	pb.RegisterCloudCoordinatorServer(s, &CloudCoordinatorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Creates a listener, registers the grpc server for coordinating
algorithms hosted in sites, and serves requests that arrive at
the listener.

No args.
*/
func ServeSites() {
	listener, err := net.Listen("tcp", config.ListenSiteIpPort)
	checkErr(err)
	fmt.Println("Coordinator: Listening for site connectors at", config.ListenSiteIpPort)
	s := grpc.NewServer()
	pb.RegisterSiteCoordinatorServer(s, &SiteCoordinatorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Helper to log errors in the coordinator.

err: Error returned by a function that should be checked
     if nil or not.
*/
func checkErr(err error) {
	if err != nil {
		fmt.Println("Coordinator:", err.Error())
	}
}