package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/golang/protobuf/proto"
	"io/ioutil"
	pb "leap/protoBuf"
	"net"
	"os"
)

var (
	config Config
)

type Config struct {
	CoordinatorIpPort string
}

var patients = []pb.Patient{{Fname: "Han", Lname: "Solo", Email: "hsolo@gmail.com", Age: 29, Gender: pb.Patient_MALE, Weight: 80, Height: 180},
	{Fname: "Mark", Lname: "Atlas", Email: "matlas@gmail.com", Age: 92, Gender: pb.Patient_MALE, Weight: 61, Height: 180},
	{Fname: "Joe", Lname: "Hum", Email: "jhum@gmail.com", Age: 85, Gender: pb.Patient_MALE, Weight: 72, Height: 184},
	{Fname: "Bill", Lname: "Blase", Email: "blase@gmail.com", Age: 22, Gender: pb.Patient_MALE, Weight: 85, Height: 174},
	{Fname: "Mary", Lname: "Swalino", Email: "mswalino@gmail.com", Age: 19, Gender: pb.Patient_FEMALE, Weight: 55, Height: 178},
	{Fname: "Milton", Lname: "Bo", Email: "mbo@gmail.com", Age: 19, Gender: pb.Patient_MALE, Weight: 78, Height: 186},
	{Fname: "Olivia", Lname: "Alos", Email: "oalos@gmail.com", Age: 30, Gender: pb.Patient_FEMALE, Weight: 50, Height: 160},
	{Fname: "Clarissa", Lname: "Vikander", Email: "cikander@gmail.com", Age: 41, Gender: pb.Patient_FEMALE, Weight: 61, Height: 155},
	{Fname: "Bruna", Lname: "Lorius", Email: "blorius@gmail.com", Age: 55, Gender: pb.Patient_FEMALE, Weight: 60, Height: 172},
	{Fname: "Anna", Lname: "Tu", Email: "atu@gmail.com", Age: 101, Gender: pb.Patient_FEMALE, Weight: 65, Height: 150}}

/*
Parses user flags and creates config using the given flags.
If a flag is absent, use the default flag given in the
config.json file.

No args
 */
func InitializeConfig() {
	jsonFile, err := os.Open("config.json")
	checkErr(err)
	defer jsonFile.Close()
	jsonBytes, err := ioutil.ReadAll(jsonFile)
	checkErr(err)

	err = json.Unmarshal(jsonBytes, &config)
	checkErr(err)

	coordinatorIpPortPtr := flag.String("ip", config.CoordinatorIpPort, "The ip and port to listen for coordinators")
	flag.Parse()

	config.CoordinatorIpPort = *coordinatorIpPortPtr
}

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

/*
Helper to log errors in a site connector

err: Error returned by a function that should be checked
     if nil or not.
*/
func checkErr(err error) {
	if err != nil {
		fmt.Println("Site Connector:", err.Error())
		os.Exit(1)
	}
}

/*
Listens to connections from coordinator. When a connection
is accepted, a goroutine is spawned to handle the newly
accepted connection.

No args
*/
func ListenConnections() {
	listener, err := net.Listen("tcp", config.CoordinatorIpPort)
	checkErr(err)
	defer listener.Close()
	fmt.Println("Site Connector: Listening for site connections at " + config.CoordinatorIpPort)
	for {
		conn, err := listener.Accept()
		checkErr(err)
		go handleConnection(conn)
	}
}

/*
Reads all the data from the connection between a site and a
coordinator. The site connector gets this data, calls the
appropriate algorithm to perform the query, and returns the
result to the coordinator

conn: A connection established between the site connector and
      a coordinator.
*/
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
