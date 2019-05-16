package main

import (
	"fmt"
	"net"
)

/*
Run with go run *.go

Accepted Flags
- cip: Ip and port to listen for connections from cloud algos
- sip: Ip and port to listent for connection from site connectors

e.g go run *.go -cip=127.0.0.1:8000 -sip=127.0.0.1:8001
*/

func main() {
	fmt.Println("Starting coordinator")
	InitializeConfig()
	listener, err := net.Listen("tcp", config.IpPort)
	checkErr(err)
	fmt.Println("Listening for connections at:", config.IpPort)
	go ListenSites(listener)
	go ListenCloud(listener)
	// Sleep main goroutine forever
	select {}
}
