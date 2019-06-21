package main

// Run with go run *.go
//
// Accepted Flags
// - cip: Ip and port to listen for connections from cloud algos
// - sip: Ip and port to listent for connection from site connectors
//
// e.g go run *.go -cip=127.0.0.1:8000 -sip=127.0.0.1:8001

func main() {
	config := GetConfigFromFile()
	AddFileHookToLogs()
	log.Info("Starting coordinator.")
	coord = NewCoordinator(config)
	go coord.ServeSites()
	go coord.ServeCloud()
	// Sleep main goroutine forever
	select {}
}
