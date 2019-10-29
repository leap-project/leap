package main

import (
	"leap/coordinator"
)

// Run with go run *.go
//
// Accepted Flags
// - ip: Ip and port to listen for connections
// - secure: Whether to use SSL/TLS encryption
// - crt: Path to the coordinator's certificate (used with TLS)
// - key: Path to the coordinator's private key (used with TLS)
// - ca: Path to the certificate authority (used with TLS)
//
/* e.g go run coordinator-main.go -ip=127.0.0.1:50000 -secure=true -crt="../coordinator/certs/coord.crt" \
   -key="../coordinator/certs/coord.key" -ca="../certs/myCA.crt" */

func main() {
	config := coordinator.GetConfig("coord-config.json")
	coordinator.AddFileHookToLogs("logs/")
	coord := coordinator.NewCoordinator(config)
	go coord.Serve()
	// Sleep main goroutine forever
	select {}
}
