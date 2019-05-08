package coordinator

import (
	"fmt"
	"os"
)

func checkSiteErr(err error) {
	if err != nil {
		fmt.Println("Site: ", err.Error())
		os.Exit(1)
	}
}

func checkCloudErr(err error) {
	if err != nil {
		fmt.Println("Cloud: ", err.Error())
		os.Exit(1)
	}
}
