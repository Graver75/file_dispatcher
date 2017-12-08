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
    async componentWillMount() {
        //TODO: error handler
        let res = await Ajax.getFiles(this.state.owner);
        let files = await res.json();
        this.setState({files})
    }
    renderFilesInfo() {
        let renderedFilesInfo = [];
        for (let fileInfo of this.state.files) {
            renderedFilesInfo.push(
                <li>{fileInfo}</li>
            )
        }
        return renderedFilesInfo
    }
    render() {
        return (
            <ul>
                {this.renderFilesInfo()}
            </ul>
        )
    }
}