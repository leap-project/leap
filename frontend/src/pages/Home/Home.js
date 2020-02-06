import React from "react";
import "./Home.css"
import Button from "../../components/Button/Button"
import LeapService from "../../services/LeapService"

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = { queryResult: null};
        this.leapService = new LeapService();
        this.handleComputeClick = this.handleComputeClick.bind(this);
        this.ButtonElement = React.createRef();
    }

    handleComputeClick() {
        this.leapService.compute("")
            .then(res => {
            this.setState({queryResult: res});
            this.ButtonElement.current.changeState('success');
        })
            .catch(err => {
                console.log("caught error on compute click")
                this.ButtonElement.current.changeState('error');
            });
    }

    render() {
        return (
            <div className="outer-div">
                How many women in our database have been previously pregnant?
                <div>
                    <Button className='ComputeButton'
                            onClick={this.handleComputeClick}
                            state={this.state.buttonState}
                            text={"Compute"}
                            ref={this.ButtonElement}
                    />
                </div>
            </div>
        );
    }
}

export default Home