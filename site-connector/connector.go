package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"google.golang.org/grpc"
	"io/ioutil"
	pb "leap/protoBuf"
	"net"
	"os"
)

var (
	config Config
	algos = make(map[AlgoId]string)
)

type AlgoId int32

type Config struct {
	CoordinatorIpPort string
	AlgosIpPort string
}

type AlgoConnectorService struct {}
type CoordinatorConnectorService struct {}

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

	CoordinatorIpPortPtr := flag.String("cip", config.CoordinatorIpPort, "The ip and port to listen for coordinators")
	AlgosIpPortPtr := flag.String("aip", config.AlgosIpPort, "The ip and port to listen for site algorithms")
	flag.Parse()

	config.CoordinatorIpPort = *CoordinatorIpPortPtr
	config.AlgosIpPort = *AlgosIpPortPtr
}

/*
Invokes algorithm in site and returns the result of per-
forming the algorithm on the given query to the coordinator.

ctx: Carries value and cancellation signals across API
     boundaries.
req: Request created by algorithm in the cloud and issued
     by coordinator.
 */
func (s *CoordinatorConnectorService) AlgoRequest(ctx context.Context, req *pb.ComputeRequest) (*pb.ComputeResponse, error) {
	fmt.Println("Site-Connector: Compute request received")
	// TODO: Use algo id to contact appropriate algorithm
	result := count(*req.Query)
	res := pb.ComputeResponse{Response: result}
	return &res, nil
}

/*
Serves RPC calls from site algorithms.

No args.
*/
func ListenAlgos() {
	listener, err := net.Listen("tcp", config.AlgosIpPort)
	fmt.Println("Site-Connector: Listening for site algos at", config.AlgosIpPort)
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterAlgoConnectorServer(s, &AlgoConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Serves RPC calls from coordinator.

No args.
*/
func ListenCoordinator() {
	listener, err := net.Listen("tcp", config.CoordinatorIpPort)
	fmt.Println("Site-Connector: Listening for coordinator at", config.CoordinatorIpPort)
	checkErr(err)
	s := grpc.NewServer()
	pb.RegisterCoordinatorConnectorServer(s, &CoordinatorConnectorService{})
	err = s.Serve(listener)
	checkErr(err)
}

/*
Helper to log errors in a site connector.

err: Error returned by a function that should be checked
     if nil or not.
*/
func checkErr(err error) {
	if err != nil {
		fmt.Println("Site Connector:", err.Error())
		os.Exit(1)
	}
}

// TODO: Delete code below and setup redcap database
var patients = []pb.Patient{{FirstName: "Han", LastName: "Solo", Email: "hsolo@gmail.com", Age: 29, Gender: pb.Patient_MALE, Weight: 80, Height: 180},
	{FirstName: "Mark", LastName: "Atlas", Email: "matlas@gmail.com", Age: 92, Gender: pb.Patient_MALE, Weight: 61, Height: 180},
	{FirstName: "Joe", LastName: "Hum", Email: "jhum@gmail.com", Age: 85, Gender: pb.Patient_MALE, Weight: 72, Height: 184},
	{FirstName: "Bill", LastName: "Blase", Email: "blase@gmail.com", Age: 22, Gender: pb.Patient_MALE, Weight: 85, Height: 174},
	{FirstName: "Mary", LastName: "Swalino", Email: "mswalino@gmail.com", Age: 19, Gender: pb.Patient_FEMALE, Weight: 55, Height: 178},
	{FirstName: "Milton", LastName: "Bo", Email: "mbo@gmail.com", Age: 19, Gender: pb.Patient_MALE, Weight: 78, Height: 186},
	{FirstName: "Olivia", LastName: "Alos", Email: "oalos@gmail.com", Age: 30, Gender: pb.Patient_FEMALE, Weight: 50, Height: 160},
	{FirstName: "Clarissa", LastName: "Vikander", Email: "cikander@gmail.com", Age: 41, Gender: pb.Patient_FEMALE, Weight: 61, Height: 155},
	{FirstName: "Bruna", LastName: "Lorius", Email: "blorius@gmail.com", Age: 55, Gender: pb.Patient_FEMALE, Weight: 60, Height: 172},
	{FirstName: "Anna", LastName: "Tu", Email: "atu@gmail.com", Age: 101, Gender: pb.Patient_FEMALE, Weight: 65, Height: 150}}

func compare(patientVal float32, queryVal int32, operator string) bool {
	switch operator {
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
			if compare(float32(patient.Age), query.NumericValue, query.Operator) {
				count++
			}
		case "weight":
			if compare(patient.Weight, query.NumericValue, query.Operator) {
				count++
			}
		case "height":
			if compare(float32(patient.Height), query.NumericValue, query.Operator) {
				count++
			}
		}
	}
	return int32(count)
}