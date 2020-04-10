package main

import (
	siteconnector "leap/siteconn"
)

// Run with go run *.go
//
// Accepted Flags
// - config: The path to the configuration file for the site connector
//
// e.g go run connector-main.go -config=../config/conn-config.json

func main() {
	config := siteconnector.GetConfig()
	siteconnector.AddFileHookToLogs("logs/", int(config.SiteId))
	sc := siteconnector.NewSiteConnector(config)
	go sc.Serve()
	sc.Register()
	// Sleep main goroutine forever
	select {}
}
