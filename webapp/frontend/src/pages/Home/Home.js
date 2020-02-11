import React from "react";
import "./Home.css"
import Button from "../../components/Button/Button"
import ComputeService from "../../services/ComputeService"

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = { queryResult: null};
        this.computeService = new ComputeService();
        this.handleComputeClick = this.handleComputeClick.bind(this);
        this.ButtonElement = React.createRef();
    }

    handleComputeClick() {
        this.computeService.compute({dp: false, algo: "count"}).then(res => {
            console.log("Something is working");
            this.setState({queryResult: res.computationResult});
            this.ButtonElement.current.changeState('success');
        }).catch(err => {
            this.ButtonElement.current.changeState('error');
        })

        //     , res => {
        //     console.log("Something is working");
        //     this.setState({queryResult: res.computationResult});
        //     this.ButtonElement.current.changeState('success');
        // }).catch(err => {
        //     console.log("Is this the error?");
        //     console.log(err);
        //     console.log("Yes sir!");
        //     this.ButtonElement.current.changeState('error');
        // });
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