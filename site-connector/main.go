package main

/*
Run with go run *.go

Accepted Flags
- ip: Ip and port to listen for connections from coordinator

e.g go run *.go -ip=127.0.0.1:9000
*/

func main() {
	InitializeConfig()
	go ListenCoordinator()
	go ListenAlgos()
	// Sleep main goroutine forever
	select {}
}
