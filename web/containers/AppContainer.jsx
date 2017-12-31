import React from 'react';

import NodesList from './NodesList'
import NodeInfoComponent from '../components/NodeInfoComponent'

export default class AppContainer extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return (
            <main>
                <PluginList/>
                <NodeInfoComponent/>
                <NodesList/>
            </main>
        )
    }
}