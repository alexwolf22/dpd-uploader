import dpd_uploader as du
from dpd_uploader.tmp.configure import configure_upload
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

UPLOAD_BUTTON_ID = "upload-button"
UPLOAD_BUTTON_TEXT_SPAN_ID = 'upload-button-text-span'

# NOTE: Aso defined in dash_app/data_management_container/__init__.py
# to avoid circular dependency
DATA_MANAGEMENT_CONTAINER_ID = "data-management-container"


UPLOAD_API = '/upload'


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
    style=UPLOAD_BUTTON_CSS,
    service=UPLOAD_API,
    max_file_size=MAX_FILE_SIZE_MB * 1024 * 1024,
    accepted_file_types=["csv", "xls", "xlsx", "xlsb", "odf"],
    children=html.Span(id=UPLOAD_BUTTON_TEXT_SPAN_ID,
                       children="Upload New Dataset"),
)


# -----------------------------
#         Dash App
# -----------------------------

app = dash.Dash(__name__)
configure_upload(app, "~/Desktop/upload_test_data", upload_api=UPLOAD_API)
app.layout = html.Div(
    children=[
        html.H1('Demo'),
        html.Div(
            children=[
                component,
                html.Div(id='callback-output')
            ],
        ),
    ],
)

# -----------------------------
#         Callback to Test
# -----------------------------

@app.callback(
    Output('callback-output', 'children'),
    [Input(UPLOAD_BUTTON_ID, 'upload_complete'),
     Input(UPLOAD_BUTTON_ID, 'upload_in_progress'),
    Input(UPLOAD_BUTTON_ID, 'file_name')]
)
def display_output(upload_complete, upload_in_progress, file_name):
    if upload_in_progress and file_name:
        return html.Span(f"{file_name} is uploading in progress...")
    elif upload_complete and file_name:
        return html.Span(f"{file_name} finished uploading")
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True)
