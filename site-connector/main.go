package main

import (
	"fmt"
)

/*
Run with go run *.go

Accepted Flags
- ip: Ip and port to listen for connections from coordinator and site algos

e.g go run *.go -ip=127.0.0.1:9000
*/

func main() {
	fmt.Println("Site-Connector: Starting site-connector")
	InitializeConfig()
	go ListenCoordinator()
	go ListenAlgos()
	// Sleep main goroutine forever
	select {}
}
