package main

import (
	"leap/Coordinator"
)

// Run with go run *.go
//
// Accepted Flags
// - ip: Ip and port to listen for connections
//
// e.g go run coordinator-main.go -ip=127.0.0.1:8000

func main() {
	config := coordinator.GetConfig("coord-config.json")
	coordinator.AddFileHookToLogs("Logs/")
	coord := coordinator.NewCoordinator(config)
	go coord.Serve()
	// Sleep main goroutine forever
	select {}
}
