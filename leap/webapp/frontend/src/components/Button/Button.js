import React from "react";
import "./Button.css";
import ProgressButton from 'react-progress-button'

class Button extends React.Component {

    constructor(props) {
        super(props);
        this.state = {buttonState: ""}
        this.onSuccess = this.onSuccess.bind(this);
        this.onError = this.onError.bind(this);
    }

    changeState(newState) {
        this.setState({buttonState: newState});
    }

    onSuccess() {
        this.setState({buttonState: ''});
    }

    onError() {
        this.setState({buttonState: ''})
    }

    render() {
        return (
            <div>
                <ProgressButton
                    className="progButton"
                    onClick={this.props.onClick}
                    onSuccess={this.onSuccess}
                    onError={this.onError}
                    state={this.state.buttonState}>
                    {this.props.text}
                </ProgressButton>
            </div>
        )
    }

}

export default Button