package main

// Run with go run *.go
//
// Accepted Flags
// - cip: Ip and port to listen for connections from coordinator
// - aip: Ip and port to listen for connections from site algos
// - id : Id of this site
//
// e.g go run *.go -cip=127.0.0.1:50002 -aip=127.0.0.1:50003 -id=0

func main() {
	InitializeConfig()
	StartLogging()
	log.Info("Starting site-connector")
	go ListenCoordinator()
	go ListenAlgos()
	// Sleep main goroutine forever
	select {}
}
