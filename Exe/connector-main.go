package main

import (
	siteconnector "leap/SiteConnector"
)

// Run with go run *.go
//
// Accepted Flags
// - ip: Ip and port to listen for connections
// - id : Id of this site
//
// e.g go run *.go -ip=127.0.0.1:50002 -id=0

func main() {
	config := siteconnector.GetConfig("conn-config.json")
	sc := siteconnector.NewSiteConnector(config)
	siteconnector.AddFileHookToLogs("Logs/", int(config.SiteId))
	go sc.Serve()
	sc.Register()
	// Sleep main goroutine forever
	select {}
}
