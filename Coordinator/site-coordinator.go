package main

import (
	"context"
	"fmt"
	pb "leap/ProtoBuf"
	"strconv"
)

/*
Service containing the API for interactions between sites
and a coordinator.
 */
type SiteCoordinatorService struct{}


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