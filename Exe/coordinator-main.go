package main

import (
	"leap/Coordinator"
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
// e.g go run coordinator-main.go -ip=127.0.0.1:8000 -secure=false -crt="../Coordinator/Certificates/server.crt" \
// key="../Coordinator/Certificates/server.key" -ca="../Certificates/myCA.crt"

func main() {
	config := coordinator.GetConfig("coord-config.json")
	coordinator.AddFileHookToLogs("Logs/")
	coord := coordinator.NewCoordinator(config)
	go coord.Serve()
	// Sleep main goroutine forever
	select {}
}
