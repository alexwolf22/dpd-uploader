import dpd_uploader as dpdu
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html


# -----------------------------
#         Constants
# -----------------------------
UPLOADER_ID = "uploader-component"

DEFAULT_STYLE = {
    'width': '100%',
    # min-height and line-height should be the same to make
    # the centering work.
    'minHeight': '100px',
    'lineHeight': '100px',
    'textAlign': 'center',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '7px',
}

# -----------------------------
#         Dash App
# -----------------------------

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H1('Demo'),
        html.Div(
            [
                dpdu.Uploader(
                    id=UPLOADER_ID,
                    textLabel='Drag and Drop files here',
                    completedMessage='Completed: ',
                    defaultStyle=DEFAULT_STYLE,
                ),
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
    [Input(UPLOADER_ID, 'isCompleted')],
    [State(UPLOADER_ID, 'fileNames'),
     State(UPLOADER_ID, 'upload_id')],
)
def display_output(isCompleted, fileNames, upload_id):
    return html.Ul([html.Li(fileNames)])


if __name__ == '__main__':
    app.run_server(debug=True)
