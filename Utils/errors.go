package Utils

import (
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// Tells whether a grpc error means that the requested
// service is unavailable.
//
// err: An error (usually from grpc)
func IsUnavailableError(err error) bool {
	e, ok := status.FromError(err)
	if !ok {
		return false
	} else {
		return e.Code() == codes.Unavailable
	}
}
