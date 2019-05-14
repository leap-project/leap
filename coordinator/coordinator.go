package coordinator

import (
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	pb "leap/protoBuf"
	"net"
)

// TODO: Take host and ports as parameters?
const (
	CONN_HOST       = "127.0.0.1"
	CONN_PORT_SITE  = "8000"
	CONN_PORT_CLOUD = "8001"
	SITE_HOST_PORT  = CONN_HOST + ":" + CONN_PORT_SITE
	CLOUD_HOST_PORT = CONN_HOST + ":" + CONN_PORT_CLOUD
	CONN_TYPE       = "tcp"
)

type Message struct {
	msg string
}

func ListenSiteConnections() {
	listener, err := net.Listen(CONN_TYPE, SITE_HOST_PORT)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Coordinator: Listening for site connections at " + SITE_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		fmt.Println("Coordinator: Accepted connection from site algorithm")
		go handleSiteConnection(conn)
	}
}

func ListenCloudConnections() {
	listener, err := net.Listen(CONN_TYPE, CLOUD_HOST_PORT)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Coordinator: Listening for cloud connections at " + CLOUD_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		fmt.Println("Coordinator: Accepted connection from cloud algorithm")
		go handleCloudConnection(conn)
	}
}

func handleSiteConnection(conn net.Conn) {
	defer conn.Close()
	buf, err := ioutil.ReadAll(conn)
	checkErr(err)
	_, err = conn.Write(buf)
	checkErr(err)
}

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

func getResultFromSite(ipPort string, query pb.Query) []byte {
	conn, err := net.Dial("tcp", ipPort)
	checkErr(err)
	out, err := proto.Marshal(&query)
	conn.Write(out)
	buf, err := ioutil.ReadAll(conn)
	return buf
}

func checkErr(err error) {
	if err != nil {
		fmt.Println("Coordinator: ", err.Error())
	}
}