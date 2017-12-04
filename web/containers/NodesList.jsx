import React from 'react';

import Ajax from '../utils/ajax'

export default class NodesList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            nodes: []
        }
    }
    async componentWillMount() {
        //TODO: error handler
        let res = await Ajax.getNodes();
        let nodes = await res.json();
        this.setState({nodes})
    }
    renderNodes() {
        return this.state.nodes.map((node) => <li>node</li>)
    }
    render() {
        return (
            <ul>
                {this.renderNodes()}
            </ul>
        )
    }
}