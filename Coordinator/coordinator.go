package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"google.golang.org/grpc"
	"io/ioutil"
	"leap/Concurrent"
	pb "leap/ProtoBuf"
	"net"
	"os"
)

var (
	// Initial config
	config Config
	// A concurrent map with algo id as key and ip and port
	// of a cloud algo as value. Equivalent to map[int32]string.
	CloudAlgos = Concurrent.NewMap()
	// A concurrent map with algo id as key and a concurrent map
	// as a value. The map as a value uses site ids for keys and
	// the value is the ip and port to contact the site. It is
	// equivalent to map[int32]map[int32]string.
	SiteConnectors = Concurrent.NewMap()
)

// A struct that holds the ip and port that the coordinator
// listens for requests from algorithms in the cloud, and the
// ip and port it listen for requests from algorithms in dis-
// tributed sites.
type Config struct {
	ListenCloudIpPort string
	ListenSiteIpPort  string
}

// Parses user flags and creates config using the given flags.
// If a flag is absent, use the default flag given in the
// config.json file.
//
// No args.
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
}

// Creates a listener, registers the grpc server for coordinating
// algorithms hosted in the cloud, and serves requests that arrive
// at the listener.
//
// No args.
func ServeCloud() {
	listener, err := net.Listen("tcp", config.ListenCloudIpPort)
	checkErr(err)
	fmt.Println("Coordinator: Listening for cloud algos at", config.ListenCloudIpPort)
	s := grpc.NewServer()
	pb.RegisterCloudCoordinatorServer(s, &CloudCoordinatorService{})
	err = s.Serve(listener)
	checkErr(err)
}

// Creates a listener, registers the grpc server for coordinating
// algorithms hosted in sites, and serves requests that arrive at
// the listener.
//
// No args.
func ServeSites() {
	listener, err := net.Listen("tcp", config.ListenSiteIpPort)
	checkErr(err)
	fmt.Println("Coordinator: Listening for site connectors at", config.ListenSiteIpPort)
	s := grpc.NewServer()
	pb.RegisterSiteCoordinatorServer(s, &SiteCoordinatorService{})
	err = s.Serve(listener)
	checkErr(err)
}

// Helper to log errors in the coordinator.
//
// err: Error returned by a function that should be checked
//      if nil or not.
func checkErr(err error) {
	if err != nil {
		fmt.Println("Coordinator:", err.Error())
	}
}
