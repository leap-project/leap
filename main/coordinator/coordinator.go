package main

import (
	"fmt"
	"leap/coordinator"
)

func main () {
	fmt.Println("Starting coordinator")
	go coordinator.ListenSiteConnections()
	go coordinator.ListenCloudConnections()
	// Sleep main goroutine forever
	select{}
}