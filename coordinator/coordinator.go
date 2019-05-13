package coordinator

import (
	"fmt"
	"github.com/golang/protobuf/proto"
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
	defer listener.Close()
	checkErr(err)
	fmt.Println("Listening for site connections at " + SITE_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		go handleSiteConnection(conn)
	}
}

func ListenCloudConnections() {
	listener, err := net.Listen(CONN_TYPE, CLOUD_HOST_PORT)
	defer listener.Close()
	checkErr(err)
	fmt.Println("Listening for cloud connections at " + CLOUD_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		go handleCloudConnection(conn)
	}
}

func handleSiteConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	_, err := conn.Read(buf)
	checkErr(err)
	conn.Write(buf)
	// TODO: Call goroutine for site alg
}

func handleCloudConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	checkErr(err)

	query := pb.Query{}
	err = proto.Unmarshal(buf[:n], &query)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Received following message from cloud: ", query)
	response := getResultFromSite("127.0.0.1:9000", query)
	conn.Write(response)
}

func getResultFromSite(ipPort string, query pb.Query) []byte {
	conn, err := net.Dial("tcp", ipPort)
	checkErr(err)
	out, err := proto.Marshal(&query)
	conn.Write(out)
	buf := make([]byte, 1024)
	conn.Read(buf)
	return buf
}

func checkErr(err error) {
	if err != nil {
		fmt.Println("Coordinator: ", err.Error())
	}
}