import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Resumablejs from "resumablejs";


function getCookie(name) {
    /*
    * Function to get the CSRF token needed to make post request to a Django View
    */
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const CSRFTOKEN = getCookie('csrftoken');



/**
Plotly Dash compatible component which allows
large file uploads using ResumableJs
 */
export default class Uploader extends Component {

    constructor(props) {
        super(props);
        this.resumable = null;
    }

    componentDidMount() {
        /*
        Init ResumableJs Post request and needed methods
         */
        const ResumableField = new Resumablejs({
            target: this.props.service,
            fileType: this.props.accepted_file_types,
            maxFiles: 1,
            maxFileSize: this.props.max_file_size,
            testMethod: 'post',
            testChunks: false,
            headers: {'X-CSRFToken': CSRFTOKEN},
            chunkSize: this.props.chunk_size,
            simultaneousUploads: 1,
            forceChunkSize: false
        });

        this.props.setProps({
            upload_complete: false
        });

        // Enable clicking or dragging file to open upload dialog
        ResumableField.assignBrowse(this.uploader);
        ResumableField.assignDrop(this.uploader);

        // Start ResumableJs file uploading when user uploads one
        ResumableField.on('fileAdded', (_file) => {
            this.props.setProps({
                upload_complete: false,
                file_name: null,
            });
            ResumableField.upload();
        });

        // Set props to file name once upload finishes to trigger plotly dash callbacks
        ResumableField.on('fileSuccess', (file, _fileServer) => {
            this.props.setProps({
                upload_complete: true,
                file_name: file.fileName,
            });
            // Make re-upload of a file with same filename possible.
            ResumableField.removeFile(file);
        });
    }

    render() {
        return (
            <div id={this.props.id} className={this.props.className} style={this.props.style}
                 ref={node => this.uploader = node}>
                {this.props.children}
            </div>
        );
    }
}

Uploader.propTypes = {
    /**
     * The ID of this component, used to identify dash components
     * in callbacks. The ID needs to be unique across all of the
     * components in an app.
     */
    id: PropTypes.string,

    /**
     * The name of the file that was uploaded
     */
    file_name: PropTypes.string,

    /**
     * Children of this dash component
     */
    children: PropTypes.oneOfType([PropTypes.node, PropTypes.string]),

    /**
     * Allow specific file types to be uploaded
     */
    accepted_file_types: PropTypes.arrayOf(PropTypes.string),

    /**
     * Maximum file size. If `-1`, then infinite
     */
    max_file_size: PropTypes.number,

    /**
     * Minimum file size
     */
    chunk_size: PropTypes.number,

    /**
     * HTML class name of the component
     */
    className: PropTypes.string,

    /**
     * CSS styles to apply upload div
     */
    style: PropTypes.object,

    /**
     *  The boolean flag telling if upload is completed.
     */
    upload_complete: PropTypes.bool,

    /**
     * The service to send the files to
     */
    service: PropTypes.string,

    /**
     * Dash-supplied function for updating props
     */
    setProps: PropTypes.func,
};

Uploader.defaultProps = {
    file_name: null,
    max_file_size:  1024 * 1024 * 10,
    chunk_size: 1024 * 1024,
    style: {},
    upload_complete: false
};