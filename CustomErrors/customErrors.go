package CustomErrors

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
