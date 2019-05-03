package main

import (
	"fmt"
	"os"
)

func checkSiteListenerErr(err error) {
	if err != nil {
		fmt.Println("Error listening for site connections: ", err.Error())
		os.Exit(1)
	}
}

func checkCloudListenerErr(err error) {
	if err != nil {
		fmt.Println("Error listening for cloud connections: ", err.Error())
		os.Exit(1)
	}
}

func checkSiteAcceptErr(err error) {
	if err != nil {
		fmt.Println("Error accepting site connection: ", err.Error())
		os.Exit(1)
	}
}

func checkCloudAcceptErr(err error) {
	if err != nil {
		fmt.Println("Error accepting cloud connection: ", err.Error())
		os.Exit(1)
	}
}

func checkReadSiteConnErr(err error) {
	if err != nil {
		fmt.Println("Error reading site connection: ", err.Error())
	}
}

func checkReadCloudConnErr(err error) {
	if err != nil {
		fmt.Println("Error reading site connection: ", err.Error())
	}
}
