package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	pb "leap/protoBuf"
	"net"
	"os"
)

var (
	config Config
)

type Message struct {
	msg string
}

type Config struct {
	CloudIpPort string
	SiteIpPort  string
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

	cloudIpPortPtr := flag.String("cip", config.CloudIpPort, "The ip and port to listen for cloud algos")
	siteIpPortPtr := flag.String("sip", config.SiteIpPort, "The ip and port to listen for site connectors")
	flag.Parse()

	config.CloudIpPort = *cloudIpPortPtr
	config.SiteIpPort = *siteIpPortPtr
}

/*
Listens to connections from sites. When a connection is accep-
ted, a goroutine is spawned to handle the newly accepted
connection.

No args
*/
func ListenSiteConnections() {
	listener, err := net.Listen("tcp", config.SiteIpPort)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Coordinator: Listening for site connections at " + config.SiteIpPort)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		fmt.Println("Coordinator: Accepted connection from site algorithm")
		go handleSiteConnection(conn)
	}
}

/*
Listens to connections from algorithms residing in our cloud
infrastructure. When a connection is accepted, a goroutine is
spawned to handle the newly accepted connection.

No args
*/
func ListenCloudConnections() {
	listener, err := net.Listen("tcp", config.CloudIpPort)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Coordinator: Listening for cloud connections at " + config.CloudIpPort)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		fmt.Println("Coordinator: Accepted connection from cloud algorithm")
		go handleCloudConnection(conn)
	}
}

// TODO: Do something useful with this function
/*
Reads all the data from the connection between the coordinator
and a site. This data is added to a buffer and written back to
the site.

conn: A connection established between the coordinator and a
      site.
*/
func handleSiteConnection(conn net.Conn) {
	defer conn.Close()
	buf, err := ioutil.ReadAll(conn)
	checkErr(err)
	_, err = conn.Write(buf)
	checkErr(err)
}

/*
Reads all the data from the connection between the coordinator
and an algorithm in our cloud infrastructure. The data is then
unmarshalled into a query, that is sent to a site that per-
forms the query. The query result is returned to the coor-
dinator, and relayed to the cloud algorithm that issued the
request.

con: A connection established between the coordinator and an
     algorithm in the cloud.
*/
func handleCloudConnection(conn net.Conn) {
	defer conn.Close()
	buf, err := ioutil.ReadAll(conn)
	checkErr(err)
	query := pb.Query{}
	err = proto.Unmarshal(buf, &query)
	checkErr(err)
	fmt.Println("Coordinator: Received following message from cloud", query)
	response := getResultFromSite("127.0.0.1:9000", query)
	_, err = conn.Write(response)
	checkErr(err)
}

/*
Issues a query to one specific site and gets the result of
performing the query on that site's local data.

ipPort: The ip + port of the site to connect to in the format
        ip:port. E.g "127.0.0.1:8000"
query:  The query issued by the cloud algorithm that should
        be performed by a site algorithm
*/
func getResultFromSite(ipPort string, query pb.Query) []byte {
	conn, err := net.Dial("tcp", ipPort)
	checkErr(err)
	out, err := proto.Marshal(&query)
	conn.Write(out)
	buf, err := ioutil.ReadAll(conn)
	return buf
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
