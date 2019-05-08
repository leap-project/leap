package main

import (
	pb "leap/protoBuf"
	"fmt"
	"github.com/golang/protobuf/proto"
	"net"
	"leap/coordinator"
)

func main() {
	testPatient := pb.Patient{Fname: "Han",
		Lname:  "Solo",
		Email:  "hsolo@gmail.com",
		Age:    29,
		Gender: pb.Patient_MALE,
		Weight: 80.0,
		Height: 180}

	out, err := proto.Marshal(&testPatient)
	if err != nil {
		fmt.Println(err)
	}


	conn, err := net.Dial("tcp", coordinator.CLOUD_HOST_PORT)
	if err != nil {
		fmt.Println(err)
	}
	_, err = conn.Write(out)
	if err != nil {
		fmt.Println(err)
	}
	response := make([]byte, 1024)
	n, err := conn.Read(response)
	msg := string(response[:n])
	fmt.Println("This is the response: ", msg)
}
