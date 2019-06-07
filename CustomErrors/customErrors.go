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

func IsSiteUnavailableError(err error) bool {
	_, ok := err.(SiteUnavailableError)
	if ok {
		return  ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewSiteUnavailableError().message {
			return true
		} else {
			return false
		}
	}
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

func IsCoordinatorUnavailableError(err error) bool {
	_, ok := err.(CoordinatorUnavailableError)
	if ok {
		return  ok
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

func IsAlgoUnavailableError(err error) bool {
	_, ok := err.(AlgoUnavailableError)
	if ok {
		return  ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewAlgoUnavailableError().message {
			return true
		} else {
			return false
		}
	}
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

func IsCloudAlgoNotRegisteredError(err error) bool {
	_, ok := err.(CloudAlgoNotRegisteredError)
	if ok {
		return  ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewCloudAlgoNotRegisteredError().message {
			return true
		} else {
			return false
		}
	}
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

func IsSiteAlgoNotRegisteredError(err error) bool {
	_, ok := err.(SiteAlgoNotRegisteredError)
	if ok {
		return  ok
	} else {
		e, ok := status.FromError(err)
		if ok && e.Message() == NewSiteAlgoNotRegisteredError().message {
			return true
		} else {
			return false
		}
	}
	return ok
}
