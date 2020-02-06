import React from "react";
import "./Home.css"
import Button from "../../components/Button/Button"
import LeapService from "../../services/LeapService"

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = { buttonState: 'neutral', queryResult: null};
        this.leapService = new LeapService();
        this.handleComputeClick = this.handleComputeClick.bind(this);
        console.log("hereee");
    }

    handleComputeClick() {
        console.log("clicking");
        this.leapService.compute("").then(res => {
            this.setState({buttonState: 'success', queryResult: res});
        });
    }

    render() {
        return (
            <div className="outer-div">
                How many women in our database have been previously pregnant?
                <div>
                    <Button className='computeButton' onClick={this.handleComputeClick} state={this.state.buttonState} text={"Compute"} />
                </div>
            </div>
        );
    }
}

export default Home