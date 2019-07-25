package CustomErrors

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

// Error that signals that a site connector is unavailable
type SiteUnavailableError struct {
	message string
}

// Creates a new SiteUnavailableError.
//
// No args.
func NewSiteUnavailableError() SiteUnavailableError {
	return SiteUnavailableError{message: "Couldn't establish connection to site-connector."}
}

// Returns the message of the error.
//
// No args.
func (e SiteUnavailableError) Error() string {
	return e.message
}

// Tells whether a given error is a SiteUnavailableError.
//
// err: The error to be checked for type.
func IsSiteUnavailableError(err error) bool {
	_, ok := err.(SiteUnavailableError)
	if ok {
		return ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewSiteUnavailableError().message {
			return true
		} else {
			return false
		}
	}
}

// Error that signals that a coordinator is unavailable.
type CoordinatorUnavailableError struct {
	message string
}


// Creates a new CoordinatorUnavailableError.
//
// No args.
func NewCoordinatorUnavailableError() CoordinatorUnavailableError {
	return CoordinatorUnavailableError{message: "Couldn't establish connection to coordinator."}
}

// Returns the message of the error.
//
// No args.
func (e CoordinatorUnavailableError) Error() string {
	return e.message
}

// Tells whether a given error is a CoordinatorUnavailableError.
//
// err: The error to be checked for type.
func IsCoordinatorUnavailableError(err error) bool {
	_, ok := err.(CoordinatorUnavailableError)
	if ok {
		return ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewCoordinatorUnavailableError().message {
			return true
		} else {
			return false
		}
	}
	return ok
}
