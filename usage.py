import dpd_uploader as du
from dpd_uploader.tmp.configure import configure_upload
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import uuid

UPLOAD_BUTTON_ID = "upload-button"
UPLOAD_BUTTON_TEXT_SPAN_ID = 'upload-button-text-span'

# NOTE: Aso defined in dash_app/data_management_container/__init__.py
# to avoid circular dependency
DATA_MANAGEMENT_CONTAINER_ID = "data-management-container"


# ---------------------     Constants       --------------------
MAX_FILE_SIZE_MB = 1000
UPLOAD_API_ENDPOINT = '/data/file_upload'

UPLOAD_BUTTON_TEXT = "Upload New {process_name} Dataset"
UPLOAD_BUTTON_CSS = {
    'border': '.1rem dashed #ffffff',
    'height': '7vw',
    'margin-top': '4vh',
    'margin-bottom': '3vh',
    'background-color': '#4299BE',
}

# ---------------------     Components      --------------------

component = du.Uploader(
    id=UPLOAD_BUTTON_ID,
    completedMessage='Uploaded: ',
    defaultStyle=UPLOAD_BUTTON_CSS,
    completeStyle=UPLOAD_BUTTON_CSS,
    uploadingStyle={**{'lineHeight': '0px'}, **UPLOAD_BUTTON_CSS},
    maxFiles=1,
    simultaneousUploads=1,
    startButton=False,
    cancelButton=False,
    pauseButton=False,
    maxFileSize=MAX_FILE_SIZE_MB * 1024 * 1024,
    filetypes=["csv", "xls", "xlsx", "xlsb", "odf"],
    upload_id=str(uuid.uuid1()),
    chunkSize=10000,
)


# -----------------------------
#         Dash App
# -----------------------------

app = dash.Dash(__name__)
configure_upload(app, "/Users/alex.wolf/Desktop/upload_test_data")
app.layout = html.Div(
    [
        html.H1('Demo'),
        html.Div(
            [
                component,
                html.Div(id='callback-output'),
            ],
            style={  # wrapper div style
                'textAlign': 'center',
                'width': '600px',
                'padding': '10px',
                'display': 'inline-block'
            }),
    ],
    style={
        'textAlign': 'center',
    },
)

# -----------------------------
#         Callback to Test
# -----------------------------

@app.callback(
    Output('callback-output', 'children'),
    [Input(UPLOAD_BUTTON_ID, 'isCompleted')],
    [State(UPLOAD_BUTTON_ID, 'fileNames'),
     State(UPLOAD_BUTTON_ID, 'upload_id')],
)
def display_output(isCompleted, fileNames, upload_id):
    return html.Ul([html.Li(fileNames)])


if __name__ == '__main__':
    app.run_server(debug=True)
