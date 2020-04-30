package main

import (
	"leap/coordinator"
)

// Run with go run *.go
//
// Accepted Flags
// - config: Path to the configuration file
//
// e.g go run coordinator-main.go -config=../config/coord-config.json

func main() {
	coordinator.AddFileHookToLogs("logs/")
	config := coordinator.GetConfig()
	coord := coordinator.NewCoordinator(config)
	go coord.Serve()
	// Sleep main goroutine forever
	select {}
}
