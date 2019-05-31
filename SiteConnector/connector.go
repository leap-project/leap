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

/*
A struct that holds the ip and port that the site connector
listens for requests from algorithms in the site, the ip
and port it listen for requests from the coordinator, and
the ip and port to contact the coordinator.
 */
type Config struct {
	ListenCoordinatorIpPort string
	ListenAlgosIpPort string
	CoordinatorIpPort string
}

var (
	siteId int32
	config Config
	algos = make(map[int32]string)
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
	SiteIdPtr := flag.Int("id", 0, "The id of a site")
	flag.Parse()

	config.ListenAlgosIpPort = *CoordinatorIpPortPtr
	config.ListenCoordinatorIpPort = *AlgosIpPortPtr
	siteId = int32(*SiteIdPtr)
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