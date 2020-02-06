import React from "react";
import "./Button.css";
import ProgressButton from 'react-progress-button'

function Button(props) {
    return (
        <div>
            <ProgressButton onClick={() => props.handleClick()} state={'loading'}>
                Compute
            </ProgressButton>
        </div>
    )
}

export default Button