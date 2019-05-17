package main

import (
	"fmt"
)

/*
Run with go run *.go

Accepted Flags
- cip: Ip and port to listen for connections from cloud algos
- sip: Ip and port to listent for connection from site connectors

e.g go run *.go -cip=127.0.0.1:8000 -sip=127.0.0.1:8001
*/

func main() {
	fmt.Println("Coordinator: Starting coordinator")
	InitializeConfig()
	go ListenSites()
	go ListenCloud()
	// Sleep main goroutine forever
	select {}
}
