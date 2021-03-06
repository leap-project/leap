import React from "react";
import Flexbox from "flexbox-react"

import "./Home.css"
import SimpleTable from "../../components/SimpleTable/SimpleTable";
import QuestionTable from "../../components/QuestionTable/QuestionTable";
import Divider from '@material-ui/core/Divider';
import ComputeService from '../../services/ComputeService'
import SiteService from "../../services/SiteService";
import {COUNT_ALGO} from "../../codes.js"

function createSiteIdList(sites) {
    let siteIds = [];
    if (sites.sites !== undefined) {
        sites.sites.forEach(site => {
            siteIds.push(site.site_id);
        });
    }
    return siteIds;
}

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {queryResult: [], sites: []};
        this.computeService = new ComputeService();
        this.siteService = new SiteService();
        this.handleComputeClick = this.handleComputeClick.bind(this);
        this.ButtonElement = React.createRef();
        this.QuestionTableElement = React.createRef()
    }

    componentDidMount() {
        this.siteService.getSites().then(sites => {
            this.setState({sites: sites})

        })
    }

    handleComputeClick() {
        let siteIds = createSiteIdList(this.state.sites);
        this.computeService.compute({dp: false, algo: COUNT_ALGO, selector:  "[age] > 50 and [bmi] < 25", sites: siteIds}).then(res => {
            this.setState({queryResult: [res]});
            this.ButtonElement.current.changeState('success');
        }).catch(err => {
            this.setState({queryResult: []});
            this.ButtonElement.current.changeState('error');
        })
    }

    render() {
        return (
            <Flexbox flexDirection="column">
                <Flexbox>
                    <SimpleTable sites={this.state.sites}/>
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