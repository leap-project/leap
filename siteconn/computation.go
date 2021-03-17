package siteconnector

import (
	"time"
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"github.com/golang/protobuf/proto"
	pb "leap/proto"
	"leap/utils"
	"io"
)

// Invokes map function in site and returns the result of run-
// ning the function on the local data.
//
// ctx: Carries value and cancellation signals across API
//      boundaries.
// req: Map request containing user defined functions.
func (sc *SiteConnector) Map(connectorStream pb.SiteConnector_MapServer) (error) {
	req, err := receiveMapRequestStream(connectorStream)
	checkErr(sc, err)
	currentTime := time.Now().UnixNano()
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Start iteration")
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Info("Received map request.")
	sc.PendingRequests.Set(req.Id, req.Id)
	conn, err := sc.Dial(sc.Conf.AlgoIpPort, sc.Conf.SiteAlgoCN)

	checkErr(sc, err)
	defer conn.Close()

	client := pb.NewSiteAlgoClient(conn)
	//ctx, cancel := context.WithTimeout(context.Background(), time.Second*10000)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	siteAlgoStream, err := client.Map(ctx)

	err = sendMapRequestStream(req, siteAlgoStream)
	checkErr(sc, err)
	res, err := receiveMapResponseStream(siteAlgoStream)
	checkErr(sc, err)

	if utils.IsUnavailableError(err) {
		sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Warn("Site Algo is unavailable.")
		checkErr(sc, err)
		return status.Error(codes.Unavailable, "Site algo is unavailable")
	} else if err != nil {
		sc.Log.WithFields(logrus.Fields{"request-id": req.Id}).Error(err)
		return err
	}

	currentTime = time.Now().UnixNano()
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("Begin send to coordinator")

	err = sendMapResponseStream(res, connectorStream)

	currentTime = time.Now().UnixNano()
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End send to coordinator")

	currentTime = time.Now().UnixNano()
	sc.Log.WithFields(logrus.Fields{"request-id": req.Id, "unix-nano": currentTime}).Info("End iteration")
	return err
}

// Receives a stream of bytes from the coordinator
//
// stream: Stream containing the bytes to be received
func receiveMapRequestStream(stream pb.SiteConnector_MapServer) (*pb.MapRequest, error) {
	recvBuf := []byte{}
	for {
	    chunk, err := stream.Recv()
	    if err == io.EOF {
		break
	    }

	    if err != nil {
	        return nil, err
	    }

	    recvBuf = append(recvBuf, chunk.Chunk...)
	}
	req := &pb.MapRequest{}
	proto.Unmarshal(recvBuf, req)
	return req, nil
}

// Sends a stream of bytes to coordinator
//
// results: List of map responses to turn into a bytes stream
// stream:  Grpc stream where the bytes are sent
func sendMapResponseStream(results *pb.MapResponse, stream pb.SiteConnector_MapServer) error {
	sendBuf, err := proto.Marshal(results)
	chunkSize := 64 * 1024
	for currByte := 0; currByte < len(sendBuf); currByte += chunkSize {
	    chunk := &pb.MapResponseChunk{}
	    if currByte + chunkSize > len(sendBuf) {
	        chunk.Chunk = sendBuf[currByte:len(sendBuf)]
	    } else {
	        chunk.Chunk = sendBuf[currByte: currByte + chunkSize]
	    }

	    if err = stream.Send(chunk); err != nil {
	        return err
	    }
	}
	return nil
}

// Sends a map request as a stream of bytes to the site algo
//
// req:    Request that is marshaled and sent as chunks
// stream: Grpc stream where bytes are sent
func sendMapRequestStream(req *pb.MapRequest, stream pb.SiteAlgo_MapClient) error {
	sendBuf, err := proto.Marshal(req)
	chunkSize := 64 * 1024
	for currByte := 0; currByte < len(sendBuf); currByte += chunkSize {
	    chunk := &pb.MapRequestChunk{}
	    if currByte + chunkSize > len(sendBuf) {
	        chunk.Chunk = sendBuf[currByte:len(sendBuf)]
	    } else {
	        chunk.Chunk = sendBuf[currByte: currByte + chunkSize]
	    }

	    if err = stream.Send(chunk); err != nil {
	        return err
	    }
	}
	stream.CloseSend()
	return nil
}

// Receives a map response as a stream of bytes from the site algo
//
// stream: Grpc stream where bytes are sent 
func receiveMapResponseStream(stream pb.SiteAlgo_MapClient) (*pb.MapResponse, error) {
	recvBuf := []byte{}
	for {
	    chunk, err := stream.Recv()
	    if err == io.EOF {
	        break
	    }

	    if err != nil {
	        return nil, err
	    }

	    recvBuf = append(recvBuf, chunk.Chunk...)
	}

	res := &pb.MapResponse{}
	proto.Unmarshal(recvBuf, res)
	return res, nil
}
