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
        let renderedNodes = [];
        for (let node in this.state.nodes) {
            renderedNodes.push(<li>{node}: {this.state.nodes[node]}</li>)
        }
        return renderedNodes
    }
    render() {
        return (
            <ul>
                {this.renderNodes()}
            </ul>
        )
    }
}