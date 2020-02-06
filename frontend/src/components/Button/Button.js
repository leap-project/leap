import React from "react";
import "./Button.css";
import ProgressButton from 'react-progress-button'

class Button extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <ProgressButton onClick={this.props.onClick()} state={'loading'}>
                    {this.props.text}
                </ProgressButton>
            </div>
        )
    }

}

export default Button