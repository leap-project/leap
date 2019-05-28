package main

import (
	"context"
	pb "leap/ProtoBuf"
)


type SiteId int32
type SiteCoordinatorService struct{}


func (s *SiteCoordinatorService) RegisterAlgo(ctx context.Context, req *pb.SiteAlgoRegReq) (*pb.SiteAlgoRegRes, error) {
	return nil, nil
}