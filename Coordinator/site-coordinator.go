package main

import (
	"context"
	"fmt"
	pb "leap/ProtoBuf"
	"strconv"
)

// Service containing the API for interactions between sites
// and a coordinator.
type SiteCoordinatorService struct{}

// Registers a ste algorithm at a coordinator. This allows
// cloud algorithms to send compute requests to registered
// site algos.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: A registration request with the site and algo id
//      of the algorithm to be registered.
func (s *SiteCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.SiteRegReq) (*pb.SiteAlgoRegRes, error) {
	fmt.Println("Coordinator: Registration request received")

	siteId := req.SiteId
	algoId := req.Req.AlgoId
	ipPort := req.SiteIpPort

	_, ok := SiteConnectors[algoId]
	if ok {
		SiteConnectors[algoId][siteId] = ipPort
	} else {
		SiteConnectors[algoId] = make(map[int32]string)
		SiteConnectors[algoId][siteId] = ipPort
	}

	msg := "Algo " + strconv.Itoa(int(algoId)) + " registered successfully"
	response := pb.SiteAlgoRegRes{Success: true, Msg: msg}
	return &response, nil
}