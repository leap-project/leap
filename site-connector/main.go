package main

import "net"

/*
Run with go run *.go

Accepted Flags
- ip: Ip and port to listen for connections from coordinator and site algos

e.g go run *.go -ip=127.0.0.1:9000
*/

func main() {
	InitializeConfig()
	listener, err := net.Listen("tcp", config.IpPort)
	checkErr(err)
	go ListenCoordinator(listener)
	go ListenAlgos(listener)
	// Sleep main goroutine forever
	select {}
}
