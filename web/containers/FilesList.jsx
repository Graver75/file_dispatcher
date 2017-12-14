import React from 'react';

import Ajax from '../utils/ajax'

export default class FilesList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            files: [],
            owner: props.id
        };

        this.handleClick = this.handleClick.bind(this)
    }
    async componentWillMount() {
        //TODO: error handler
        let res = await Ajax.getFiles(this.state.owner);
        let files = await res.json();
        this.setState({files});
    }
    handleClick(evt) {
        return (name) => {
            evt.preventDefault();
            Ajax.getFile(this.state.owner, name)
        }
    }
    renderFilesInfo() {
        let renderedFilesInfo = [];
        for (let fileInfo of this.state.files) {
            renderedFilesInfo.push(
                <li onClick={this.handleClick(fileInfo)}>{fileInfo}</li>
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