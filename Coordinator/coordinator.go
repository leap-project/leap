package coordinator

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
	"sync"
)

// A struct that holds the ip and port that the coordinator
// listens for requests from algorithms in the cloud, and the
// ip and port it listen for requests from algorithms in dis-
// tributed sites.
type Config struct {
	IpPort string
}

type Coordinator struct {
	// Initial config
	Conf Config
	// Logging tool
	Log *logrus.Entry
	// TODO: Deal with overflow
	// NextId
	NextId int64
	// Lock for NextId
	IdMux sync.Mutex
	// A concurrent map with request id as key and value. It re-
	// presents the client requests that are being computed.
	PendingRequests *Concurrent.Map
	// A concurrent map with site id as key and the ip and
	// port of the site as a value.
	SiteConnectors *Concurrent.Map
}

// Creates a new coordinator with the configurations given
// as the parameter.
//
// config: The ip and port configuration of the coordinator.
func NewCoordinator(config Config) *Coordinator {
	return &Coordinator{Conf: config,
						Log: logrus.WithFields(logrus.Fields{"node": "coordinator"}),
						NextId: 0,
						PendingRequests: Concurrent.NewMap(),
						SiteConnectors: Concurrent.NewMap(),
}
}

// Parses user flags and creates config using the given flags.
// If a flag is absent, use the default flag given in the
// config.json file.
//
// filePath: The path to a file with config information.
func GetConfig(filePath string) Config {
	jsonFile, _ := os.Open(filePath)
	defer jsonFile.Close()
	jsonBytes, _ := ioutil.ReadAll(jsonFile)

	config := Config{}
	json.Unmarshal(jsonBytes, &config)

	IpPortPtr := flag.String("ip", config.IpPort, "The ip and port of the coordinator")
	flag.Parse()

	config.IpPort = *IpPortPtr
	return config
}

// Creates a 'Logs' directory if one doesn't exist, and creates
// a file to output the log files. This function also adds a
// hook to logrus, so that it can write to the file in text
// format, and display messages in terminal with colour.
//
// filepath: The path to the file where the logs should be added.
// dirpath:  The path to the directory where the logs will be located.
func AddFileHookToLogs(dirPath string) {
	_, err := os.Stat(dirPath)
	if os.IsNotExist(err) {
		os.Mkdir(dirPath, os.ModePerm)
	}

	filePath := dirPath + "coordinator.log"
	os.Create(filePath)

	hook := lfshook.NewHook(lfshook.PathMap{}, &logrus.JSONFormatter{})
	hook.SetDefaultPath(filePath)
	logrus.AddHook(hook)
}

// Creates a listener, registers the grpc server for the
// coordinator, and serves requests that arrive at the
// listener.
//
// No args.
func (c *Coordinator) Serve() {
	listener, err := net.Listen("tcp", c.Conf.IpPort)
	checkErr(c, err)
	c.Log.WithFields(logrus.Fields{"ip-port": c.Conf.IpPort}).Info("Listening for requests.")
	s := grpc.NewServer()
	pb.RegisterCoordinatorServer(s, c)
	err = s.Serve(listener)
	checkErr(c, err)
}

// Stops the grpc server for the coordinator. Server will
// stop accepting connecitons and will close all the connected
// connections.
//
// No args.
func (c *Coordinator) Stop() {
	c.Stop()
}

// Helper to log errors in the coordinator.
//
// coord: Coordinator instance
// err: Error returned by a function that should be checked
//      if nil or not.
func checkErr(c *Coordinator, err error) {
	if err != nil {
		c.Log.Error(err.Error())
	}
}
