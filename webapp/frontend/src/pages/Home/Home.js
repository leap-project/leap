import React from "react";
import Flexbox from "flexbox-react"

import "./Home.css"
import ComputeService from "../../services/ComputeService"
import SimpleTable from "../../components/SimpleTable/SimpleTable";
import QuestionTable from "../../components/QuestionTable/QuestionTable";
import Divider from '@material-ui/core/Divider';

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {queryResult: []};
        this.computeService = new ComputeService();
        this.handleComputeClick = this.handleComputeClick.bind(this);
        this.ButtonElement = React.createRef();
    }

    handleComputeClick() {
        this.computeService.compute({dp: false, algo: "count"}).then(res => {
            this.setState({queryResult: [128]});
            this.ButtonElement.current.changeState('success');
        }).catch(err => {
            this.ButtonElement.current.changeState('error');
        })
    }

    render() {
        return (
            <Flexbox flexDirection="column">
                <Flexbox>
                    <SimpleTable/>
                </Flexbox>
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Divider />
                <Flexbox>
                    <QuestionTable buttonState={this.state.buttonState} buttonClick={this.handleComputeClick}
                                   buttonRef={this.ButtonElement} queryResult={this.state.queryResult}/>
                </Flexbox>
            </Flexbox>
        );
    }
}

export default Home

// <Flexbox flexDirection="row">
//     <div className="questionText"> How many women in our database have been previously pregnant?</div>
// <Button className='ComputeButton'
// onClick={this.handleComputeClick}
// state={this.state.buttonState}
// text={"Compute"}
// ref={this.ButtonElement}
// />
// </Flexbox>