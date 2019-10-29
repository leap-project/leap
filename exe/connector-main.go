package main

import (
	siteconnector "leap/siteconn"
)

// Run with go run *.go
//
// Accepted Flags
// - ip: Ip and port to listen for connections
// - id : Id of this site
//
// e.g go run connector-main.go -ip=127.0.0.1:50001 -cip="127.0.0.1:50001" -aip="127.0.0.1:60000" -id=0

func main() {
	config := siteconnector.GetConfig("conn-config.json")
	sc := siteconnector.NewSiteConnector(config)
	siteconnector.AddFileHookToLogs("logs/", int(config.SiteId))
	go sc.Serve()
	sc.Register()
	// Sleep main goroutine forever
	select {}
}
