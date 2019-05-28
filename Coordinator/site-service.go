package main

import (
	"context"
	pb "leap/ProtoBuf"
)

/*
Service containing the API for interactions between sites
and a coordinator.
 */
type SiteCoordinatorService struct{}


func (s *SiteCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	return nil, nil
}