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
	"strconv"
)

var (
	// Site Connector
	siteConn *SiteConnector
	// Logging tool
	log = logrus.WithFields(logrus.Fields{"node-type": "site-connector"})
)

type SiteConnector struct {
	// Initial Config
	Conf Config
	// List of Algos in this site
	SiteAlgos *Concurrent.Map
}

// A struct that holds the ip and port that the site connector
// listens for requests from algorithms in the site, the ip
// and port it listen for requests from the coordinator, and
// the ip and port to contact the coordinator.
type Config struct {
	ListenCoordinatorIpPort string
	ListenAlgosIpPort       string
	CoordinatorIpPort       string
	SiteId                  int32
}

// Creates a new site connector with the configurations given
// as the parameter.
//
// config: The ip and port configurations of the site connector.
func NewSiteConnector(config Config) *SiteConnector {
	return &SiteConnector{Conf: config, SiteAlgos: Concurrent.NewMap()}
}

// Parses user flags and creates config using the given flags.
// If a flag is absent, use the default flag given in the
// config.json file.
//
// No args
func GetConfigFromFile() Config {
	jsonFile, err := os.Open("config.json")
	checkErr(err)
	defer jsonFile.Close()
	jsonBytes, err := ioutil.ReadAll(jsonFile)
	checkErr(err)

	config := Config{}
	err = json.Unmarshal(jsonBytes, &config)
	checkErr(err)

	SiteIdPtr := flag.Int("id", 0, "The id of a site")
	CoordinatorIpPortPtr := flag.String("cip", config.ListenCoordinatorIpPort, "The ip and port to listen for coordinators")
	AlgosIpPortPtr := flag.String("aip", config.ListenAlgosIpPort, "The ip and port to listen for site algorithms")
	CoordinatorPtr := flag.String("c", config.CoordinatorIpPort, "The ip and port of the coordinator to be contacted")
	flag.Parse()

	config.SiteId = int32(*SiteIdPtr)
	config.ListenCoordinatorIpPort = *CoordinatorIpPortPtr
	config.ListenAlgosIpPort = *AlgosIpPortPtr
	config.CoordinatorIpPort = *CoordinatorPtr
	return config
}

// Creates a 'Logs' directory if one doesn't exist, and creates
// a file to output the log files. This function also adds a
// hook to logrus, so that it can write to the file in text
// format, and display messages in terminal with colour.
//
// No args.
func AddFileHookToLogs(siteId int) {
	_, err := os.Stat("Logs/")
	if os.IsNotExist(err) {
		os.Mkdir("Logs/", os.ModePerm)
	}

	filePath := "Logs/site" + strconv.Itoa(siteId) + ".log"
	_, err = os.Create(filePath)
	checkErr(err)

	hook := lfshook.NewHook(lfshook.PathMap{}, &logrus.JSONFormatter{})
	hook.SetDefaultPath(filePath)
	logrus.AddHook(hook)
	log = logrus.WithFields(logrus.Fields{"node": "site-connector", "site-id": siteId})
}

// Serves RPC calls from site algorithms.
//
// No args.
func (sc *SiteConnector) ListenAlgos() {
	listener, err := net.Listen("tcp", sc.Conf.ListenAlgosIpPort)
	log.WithFields(logrus.Fields{"ip-port": sc.Conf.ListenAlgosIpPort}).Info("Listening for site algos.")
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterAlgoConnectorServer(s, &AlgoConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

// Serves RPC calls from coordinator.
//
// No args.
func (sc *SiteConnector) ListenCoordinator() {
	listener, err := net.Listen("tcp", sc.Conf.ListenCoordinatorIpPort)
	log.WithFields(logrus.Fields{"ip-port": sc.Conf.ListenCoordinatorIpPort}).Info("Listening for coordinator.")
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterCoordinatorConnectorServer(s, &CoordinatorConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

// Helper to log errors in a site connector.
//
// err: Error returned by a function that should be checked
//      if nil or not.
func checkErr(err error) {
	if err != nil {
		log.Error(err.Error())
	}
}