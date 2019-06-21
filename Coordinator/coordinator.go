package main

import (
	"encoding/json"
	"flag"
	"github.com/rifflock/lfshook"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"io/ioutil"
	"leap/Concurrent"
	pb "leap/ProtoBuf"
	"net"
	"os"
)

var (
	// Coordinator
	coord *Coordinator
	// Logging tool
	log = logrus.WithFields(logrus.Fields{"node": "coordinator"})
)

type Coordinator struct {
	// Initial config
	Conf Config
	// A concurrent map with algo id as key and ip and port
	// of a cloud algo as value. Equivalent to map[int32]string.
	CloudAlgos *Concurrent.Map
	// A concurrent map with algo id as key and a concurrent map
	// as a value. The map as a value uses site ids for keys and
	// the value is the ip and port to contact the site. It is
	// equivalent to map[int32]map[int32]string.
	SiteConnectors *Concurrent.Map
}

// A struct that holds the ip and port that the coordinator
// listens for requests from algorithms in the cloud, and the
// ip and port it listen for requests from algorithms in dis-
// tributed sites.
type Config struct {
	ListenCloudIpPort string
	ListenSiteIpPort  string
}

// Creates a new coordinator with the configurations given
// as the parameter.
//
// config: The ip and port configuration of the coordinator.
func NewCoordinator(config Config) *Coordinator {
	return &Coordinator{Conf: config, CloudAlgos: Concurrent.NewMap(), SiteConnectors: Concurrent.NewMap()}
}

// Parses user flags and creates config using the given flags.
// If a flag is absent, use the default flag given in the
// config.json file.
//
// No args.
func GetConfigFromFile() Config {
	jsonFile, err := os.Open("config.json")
	checkErr(err)
	defer jsonFile.Close()
	jsonBytes, err := ioutil.ReadAll(jsonFile)
	checkErr(err)

	config := Config{}
	err = json.Unmarshal(jsonBytes, &config)
	checkErr(err)

	CloudIpPortPtr := flag.String("cip", config.ListenCloudIpPort, "The ip and port the coordinator is listening for cloud connections")
	SiteIpPortPtr := flag.String("sip", config.ListenSiteIpPort, "The ip and port the coordinator is listening for site connections")
	flag.Parse()

	config.ListenCloudIpPort = *CloudIpPortPtr
	config.ListenSiteIpPort = *SiteIpPortPtr
	return config
}

// Creates a 'Logs' directory if one doesn't exist, and creates
// a file to output the log files. This function also adds a
// hook to logrus, so that it can write to the file in text
// format, and display messages in terminal with colour.
//
// No args.
func AddFileHookToLogs() {
	_, err := os.Stat("Logs/")
	if os.IsNotExist(err) {
		os.Mkdir("Logs/", os.ModePerm)
	}

	filePath := "Logs/coordinator.log"
	_, err = os.Create(filePath)
	checkErr(err)

	hook := lfshook.NewHook(lfshook.PathMap{}, &logrus.JSONFormatter{})
	hook.SetDefaultPath(filePath)
	logrus.AddHook(hook)
}

// Creates a listener, registers the grpc server for coordinating
// algorithms hosted in the cloud, and serves requests that arrive
// at the listener.
//
// No args.
func (c *Coordinator) ServeCloud() {
	listener, err := net.Listen("tcp", c.Conf.ListenCloudIpPort)
	checkErr(err)
	log.WithFields(logrus.Fields{"ip-port": c.Conf.ListenCloudIpPort}).Info("Listening for cloud algos.")
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
func (c *Coordinator) ServeSites() {
	listener, err := net.Listen("tcp", c.Conf.ListenSiteIpPort)
	checkErr(err)
	log.WithFields(logrus.Fields{"ip-port": c.Conf.ListenSiteIpPort}).Info("Listening for site connectors.")
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
		log.Error(err.Error())
	}
}
