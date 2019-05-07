package coordinator

import (
	"fmt"
	"github.com/golang/protobuf/proto"
	"net"
	pb "leap/protoBuf"
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
	checkSiteListenerErr(err)
	fmt.Println("Listening for site connections at " + SITE_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkSiteAcceptErr(err)
		go handleSiteConnection(conn)
	}
}

func handleSiteConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	checkReadSiteConnErr(err)

	patient := pb.Patient{}
	err = proto.Unmarshal(buf[:n], &patient)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Received following message from site: ", patient)
	conn.Write([]byte("Test Site Received"))
	// TODO: Call goroutine for site alg
}

func ListenCloudConnections() {
	listener, err := net.Listen(CONN_TYPE, CLOUD_HOST_PORT)
	defer listener.Close()
	checkCloudListenerErr(err)
	fmt.Println("Listening for cloud connections at " + CLOUD_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkCloudAcceptErr(err)
		go handleCloudConnection(conn)
	}
}

func handleCloudConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	checkReadCloudConnErr(err)

	patient := pb.Patient{}
	err = proto.Unmarshal(buf[:n], &patient)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("Received following message from cloud: ", patient)
	conn.Write([]byte("Test Cloud Received"))
	// TODO: Call goroutine for cloud alg
}