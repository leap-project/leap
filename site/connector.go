package site

import (
	"fmt"
	"github.com/golang/protobuf/proto"
	pb "leap/protoBuf"
	"net"
	"os"
)

const (
	CONN_HOST       = "127.0.0.1"
	CONN_PORT_SITE  = "9000"
	CONN_PORT_CLOUD = "9001"
	SITE_HOST_PORT  = CONN_HOST + ":" + CONN_PORT_SITE
	CLOUD_HOST_PORT = CONN_HOST + ":" + CONN_PORT_CLOUD
	CONN_TYPE       = "tcp"
)

var  patients = []pb.Patient{{Fname: "Han", Lname: "Solo", Email: "hsolo@gmail.com", Age: 29, Gender: pb.Patient_MALE, Weight: 80, Height: 180},
	                         {Fname: "Mark", Lname: "Atlas", Email: "matlas@gmail.com", Age: 92, Gender: pb.Patient_MALE, Weight: 61, Height: 180},
	                         {Fname: "Joe", Lname: "Hum", Email: "jhum@gmail.com", Age: 85, Gender: pb.Patient_MALE, Weight: 72, Height: 184},
	                         {Fname: "Bill", Lname: "Blase", Email: "blase@gmail.com", Age: 22, Gender: pb.Patient_MALE, Weight: 85, Height: 174},
	                         {Fname: "Mary", Lname: "Swalino", Email: "mswalino@gmail.com", Age: 19, Gender: pb.Patient_FEMALE, Weight: 55, Height: 178},
	                         {Fname: "Milton", Lname: "Bo", Email: "mbo@gmail.com", Age: 19, Gender: pb.Patient_MALE, Weight: 78, Height: 186},
	                         {Fname: "Olivia", Lname: "Alos", Email: "oalos@gmail.com", Age: 30, Gender: pb.Patient_FEMALE, Weight: 50, Height: 160},
	                         {Fname: "Clarissa", Lname: "Vikander", Email: "cikander@gmail.com", Age: 41, Gender: pb.Patient_FEMALE, Weight: 61, Height: 155},
	                         {Fname: "Bruna", Lname: "Lorius", Email: "blorius@gmail.com", Age: 55, Gender: pb.Patient_FEMALE, Weight: 60, Height: 172},
	                         {Fname: "Anna", Lname: "Tu", Email: "atu@gmail.com", Age: 101, Gender: pb.Patient_FEMALE, Weight: 65, Height: 150}}

func compare(patientVal float32, queryVal int32, comparator string) bool {
	switch comparator {
	case "GT":
		return patientVal > float32(queryVal)
	case "LT":
		return patientVal < float32(queryVal)
	case "EQ":
		return patientVal == float32(queryVal)
	}
	return false
}

func count(query pb.Query) int32 {
	count := 0
	for _, patient := range patients {
		switch query.Field {
		case "age":
			if compare(float32(patient.Age), query.NumericValue, query.Comparator) {
				count++
			}
		case "weight":
			if compare(patient.Weight, query.NumericValue, query.Comparator) {
				count++
			}
		case "height":
			if compare(float32(patient.Height), query.NumericValue, query.Comparator) {
				count++
			}
		}
	}
	return int32(count)
}

func checkErr(err error) {
	if err != nil {
		fmt.Println("Site Connector: ", err.Error())
		os.Exit(1)
	}
}

func ListenConnections() {
	listener, err := net.Listen(CONN_TYPE, SITE_HOST_PORT)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Site Connector: Listening for site connections at " + SITE_HOST_PORT)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	checkErr(err)

	query := pb.Query{}
	err = proto.Unmarshal(buf[:n], &query)
	checkErr(err)
	fmt.Println("Site Connector: Received following query from coordinator", query)
	result := pb.Result{Count: count(query)}
	out, err := proto.Marshal(&result)
	conn.Write(out)
}
