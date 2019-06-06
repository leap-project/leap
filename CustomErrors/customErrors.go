package CustomErrors

import (
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func IsUnavailableError(err error) bool {
	e, ok := status.FromError(err)
	if !ok {
		return false
	} else {
		return e.Code() == codes.Unavailable
	}
}

// SiteUnavailableError
type SiteUnavailableError struct {
	message string
}

func NewSiteUnavailableError() SiteUnavailableError {
	return SiteUnavailableError{message: "Couldn't establish connection to site-connector."}
}

func (e SiteUnavailableError) Error() string {
	return e.message
}

func IsSiteUnavailableError(e error) bool {
	_, ok := e.(SiteUnavailableError)
	return ok
}

// CoordinatorUnavailableError
type CoordinatorUnavailableError struct {
	message string
}

func NewCoordinatorUnavailableError() CoordinatorUnavailableError {
	return CoordinatorUnavailableError{message: "Couldn't establish connection to coordinator."}
}

func (e CoordinatorUnavailableError) Error() string {
	return e.message
}

func IsCoordinatorUnavailableError(e error) bool {
	_, ok := e.(CoordinatorUnavailableError)
	return ok
}

// AlgoUnavailableError
type AlgoUnavailableError struct {
	message string
}

func NewAlgoUnavailableError() AlgoUnavailableError {
	return AlgoUnavailableError{message: "Couldn't establish a connection to algorithm."}
}

func (e AlgoUnavailableError) Error() string {
	return e.message
}

func IsAlgoUnavailableError(e error) bool {
	_, ok := e.(AlgoUnavailableError)
	return ok
}

// CloudAlgoNotRegistered Error
type CloudAlgoNotRegisteredError struct {
	message string
}

func NewCloudAlgoNotRegisteredError() CloudAlgoNotRegisteredError {
	return CloudAlgoNotRegisteredError{message: "This algo hasn't been registered yet."}
}

func (e CloudAlgoNotRegisteredError) Error() string {
	return e.message
}

func IsCloudAlgoNotRegisteredError(e error) bool {
	_, ok := e.(CloudAlgoNotRegisteredError)
	return ok
}

// SiteAlgoNotRegisteredError
type SiteAlgoNotRegisteredError struct {
	message string
}

func NewSiteAlgoNotRegisteredError() SiteAlgoNotRegisteredError {
	return SiteAlgoNotRegisteredError{message: "There are no site algorithms with this id."}
}

func (e SiteAlgoNotRegisteredError) Error() string {
	return e.message
}

func IsSiteAlgoNotRegisteredError(e error) bool {
	_, ok := e.(SiteAlgoNotRegisteredError)
	return ok
}
