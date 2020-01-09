// The main file for defining what a site connector looks like.

package siteconnector

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"flag"
	"google.golang.org/grpc/credentials"
	"io/ioutil"
	pb "leap/proto"
	"leap/utils"
	"net"
	"os"
	"strconv"
	"time"

	"github.com/rifflock/lfshook"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

type SiteConnector struct {
	// Initial Config
	Conf Config
	// Logging tool
	Log *logrus.Entry
	// List of pending requests in this site
	PendingRequests *utils.Map
}

// A struct that holds the ip and port that the site connector
// listens for requests from algorithms in the site, the ip
// and port it listen for requests from the coordinator, and
// the ip and port to contact the coordinator.
type Config struct {
	// Ip and port of this site connector
	IpPort            string
	// Ip and port of the coordinator
	CoordinatorIpPort string
	// Ip and port of the site algo this connector contacts
	AlgoIpPort        string
	// Id of this site
	SiteId            int32
	// Flag that determines whether to use SSL/TLS encryption
	Secure bool
	// File path to SSL/TLS certificate
	Crt string
	// File path to SSL/TLS key
	Key string
	// File path to the certificate authority crt
	CertAuth string
	// The common name of the coordinator. Used in SSL/TLS
	CoordCN string
	// The common name of the site algo. Used in SSL/TLS
	SiteAlgoCN string
}

// Creates a new site connector with the configurations given
// as the parameter.
//
// config: The ip and port configurations of the site connector.
func NewSiteConnector(config Config) *SiteConnector {
	return &SiteConnector{Conf: config,
		Log:             logrus.WithFields(logrus.Fields{"node": "site-connector", "site-id": config.SiteId}),
		PendingRequests: utils.NewMap()}
}

// Parses user flags and creates config using the given flags.
// If a flag is absent, use the default flag given in the
// config.json file.
//
// filepath: The path to the json with the config
func GetConfig(filePath string) Config {
	jsonFile, _ := os.Open(filePath)
	defer jsonFile.Close()
	jsonBytes, _ := ioutil.ReadAll(jsonFile)

	config := Config{}
	json.Unmarshal(jsonBytes, &config)

	IpPortPtr := flag.String("ip", config.IpPort, "The ip and port to listen for requests")
	CoordinatorIpPortPtr := flag.String("cip", config.CoordinatorIpPort, "The ip and port of the coordinator to be contacted")
	AlgoIpPortPtr := flag.String("aip", config.AlgoIpPort, "The ip and port of the python server to be contacted")
	SiteIdPtr := flag.Int("id", 0, "The id of a site")
	securePtr := flag.Bool("secure", config.Secure, "Whether to use SSL/TLS to encrypt and authenticate connections.")
	crtPtr := flag.String("crt", config.Crt, "The SSL/TLS certificate for the coordinator")
	keyPtr := flag.String("key", config.Key, "The SSL/TLS key for the coordinator")
	certAuthPtr := flag.String("ca", config.CertAuth, "The SSL/TLS certificate for the certificate authority")
	flag.Parse()
	flag.Parse()

	config.SiteId = int32(*SiteIdPtr)
	config.IpPort = *IpPortPtr
	config.CoordinatorIpPort = *CoordinatorIpPortPtr
	config.AlgoIpPort = *AlgoIpPortPtr
	config.Secure = *securePtr
	config.Crt = *crtPtr
	config.Key = *keyPtr
	config.CertAuth = *certAuthPtr
	return config
}

// Creates a 'Logs' directory if one doesn't exist, and creates
// a file to output the log files. This function also adds a
// hook to logrus, so that it can write to the file in text
// format, and display messages in terminal with colour.
//
// dirPath: The path to the directory where the logs shall be
//          located.
// siteId: The id of this site.
func AddFileHookToLogs(dirPath string, siteId int) {
	_, err := os.Stat(dirPath)
	if os.IsNotExist(err) {
		os.Mkdir(dirPath, os.ModePerm)
	}

	filePath := dirPath + "site" + strconv.Itoa(siteId) + ".log"
	_, err = os.Create(filePath)

	hook := lfshook.NewHook(lfshook.PathMap{}, &logrus.JSONFormatter{})
	hook.SetDefaultPath(filePath)
	logrus.AddHook(hook)
}

// Creates a listener, registers the grpc server for the
// connector, and serves requests that arrive at the
// listener.
//
// No args.
func (sc *SiteConnector) Serve() {
	listener, err := net.Listen("tcp", sc.Conf.IpPort)
	sc.Log.WithFields(logrus.Fields{"ip-port": sc.Conf.IpPort}).Info("Listening for requests.")
	checkErr(sc, err)

	var s *grpc.Server
	if sc.Conf.Secure {
		// Load coordinator certificates from disk
		cert, err := tls.LoadX509KeyPair(sc.Conf.Crt, sc.Conf.Key)
		if err != nil {
			sc.Log.Error(err)
			return
		}

		// Create certificate pool from certificate authority
		certPool := x509.NewCertPool()
		ca, err := ioutil.ReadFile(sc.Conf.CertAuth)
		if err != nil {
			sc.Log.Error(err)
			return
		}

		// Append client certificates from certificate authority
		ok := certPool.AppendCertsFromPEM(ca)
		if !ok {
			sc.Log.Error("Error when appending client certs")
		}

		// Create TLS credentials
		creds := credentials.NewTLS(&tls.Config{
			ClientAuth: tls.RequireAndVerifyClientCert,
			Certificates: []tls.Certificate{cert},
			ClientCAs: certPool,
		})

		s = grpc.NewServer(grpc.Creds(creds))

	} else {
		s = grpc.NewServer()
	}

	pb.RegisterSiteConnectorServer(s, sc)
	err = s.Serve(listener)
	checkErr(sc, err)
}

// This function registers a site-connector with a coordinator.
// The site connectors sends the coordinator its ip, port, and
// id.
//
// No args.
func (sc *SiteConnector) Register() {
	conn, err := sc.Dial(sc.Conf.CoordinatorIpPort, sc.Conf.CoordCN)
	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewCoordinatorClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
	defer cancel()

	siteRegReq := pb.SiteRegReq{SiteId: sc.Conf.SiteId, SiteIpPort: sc.Conf.IpPort}
	response, err := client.RegisterSite(ctx, &siteRegReq)
	checkErr(sc, err)
	if err == nil && response.Success {
		sc.Log.Info("Site successfully registerd.")
	} else {
		sc.Log.Warn("Was not able to register site with coordinator.")
	}
}

// This function does basically the same job as the grpc dial,
// but it loads the proper credentials and establishes a
// secure connection if the secure flag is turned on.
//
// addr: The address where you want to establish a connection
// serverName: The common name of the server to be contacted
func (sc *SiteConnector) Dial(addr string, serverName string) (*grpc.ClientConn, error) {
	if sc.Conf.Secure {
		cert, err := tls.LoadX509KeyPair(sc.Conf.Crt, sc.Conf.Key)
		checkErr(sc, err)

		certPool := x509.NewCertPool()
		ca, err := ioutil.ReadFile(sc.Conf.CertAuth)
		checkErr(sc, err)

		certPool.AppendCertsFromPEM(ca)
		creds := credentials.NewTLS(&tls.Config{
			ServerName: serverName,
			Certificates: []tls.Certificate{cert},
			RootCAs: certPool,
		})

		return grpc.Dial(addr, grpc.WithTransportCredentials(creds))

	} else {
		return grpc.Dial(addr, grpc.WithInsecure())
	}
}

// TODO: Add request id to checkErr
// Helper to log errors in a site connector.
//
// sc:  Site connector instance (holds logging tool)
// err: Error returned by a function that should be checked
//      if nil or not.
func checkErr(sc *SiteConnector, err error) {
	if err != nil {
		sc.Log.Error(err.Error())
	}
}
