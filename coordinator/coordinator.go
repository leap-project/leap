package main

import (
	"fmt"
	"net"
)

// TODO: Take host and ports as parameters?
const (
	CONN_HOST = "127.0.0.1"
	CONN_PORT_SITE = "8000"
	CONN_PORT_CLOUD = "8001"
	CONN_TYPE = "tcp"
)

type Message struct {
	msg string
}

func listenSiteConnections() {
	listener, err := net.Listen(CONN_TYPE, CONN_HOST + ":" + CONN_PORT_SITE)
	defer listener.Close()
	checkSiteListenerErr(err)
	fmt.Println("Listening for site connections at " + CONN_HOST + ":" + CONN_PORT_SITE)
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
	msg := string(buf[:n])
	fmt.Println("Received following message from site: ", msg)
	conn.Write([]byte("Test Site Received"))
	// TODO: Call goroutine for site alg
}

func listenCloudConnections() {
	listener, err := net.Listen(CONN_TYPE, CONN_HOST + ":" + CONN_PORT_CLOUD)
	defer listener.Close()
	checkCloudListenerErr(err)
	fmt.Println("Listening for cloud connections at " + CONN_HOST + ":" + CONN_PORT_CLOUD)
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
	msg := string(buf[:n])
	fmt.Println("Received following message from cloud: ", msg)
	conn.Write([]byte("Test Cloud Received"))
	// TODO: Call goroutine for cloud alg
}

func main () {
	fmt.Println("Starting coordinator")
	go listenSiteConnections()
	go listenCloudConnections()
	// Sleep main goroutine forever
	select{}
}