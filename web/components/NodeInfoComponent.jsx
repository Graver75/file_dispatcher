import React from 'react';

import Ajax from '../utils/ajax';

export default class NodeInfoComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            info: props.info || {}
        }
    }
    async componentWillMount() {
        //TODO: error handler
        let res = await Ajax.getNodeInfo(this.state.info.id);
        let info = await res.json();
        this.setState({info})

    }
    render() {
        return (
            //TODO SASS classes
            <div>
                <p>ID: {this.state.info.id}</p>
                <p>IP: {this.state.info.ip}</p>
                <p>port: {this.state.info.port}</p>
            </div>
        )
    }
}