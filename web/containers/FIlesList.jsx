import React from 'react';

import Ajax from '../utils/ajax'

export default class FilesList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            files: [],
            owner: props.id
        }
    }
    componentWillMount() {
        //TODO: error handler
        Ajax.getFiles(this.state.owner)
            .catch(console.log)
            .then((files) => {
                this.setState({files})
            })
    }
    render() {

    }
}