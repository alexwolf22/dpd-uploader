# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Uploader(Component):
    """An Uploader component.
Plotly Dash compatible component which allows
large file uploads using ResumableJs

Keyword arguments:
- children (a list of or a singular dash component, string or number | string; optional): Children of this dash component
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- file_name (string; optional): The name of the file that was uploaded
- accepted_file_types (list of strings; optional): Allow specific file types to be uploaded
- max_file_size (number; default 1024 * 1024 * 10): Maximum file size. If `-1`, then infinite
- chunk_size (number; default 1024 * 1024): Minimum file size
- className (string; optional): HTML class name of the component
- style (dict; optional): CSS styles to apply upload div
- upload_in_progress (boolean; default False): Boolean flag telling if an upload is in progress completed
- upload_complete (boolean; default False): Boolean flag telling for marking if upload is completed
- service (string; optional): The service to send the files to"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, file_name=Component.UNDEFINED, accepted_file_types=Component.UNDEFINED, max_file_size=Component.UNDEFINED, chunk_size=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, upload_in_progress=Component.UNDEFINED, upload_complete=Component.UNDEFINED, service=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'file_name', 'accepted_file_types', 'max_file_size', 'chunk_size', 'className', 'style', 'upload_in_progress', 'upload_complete', 'service']
        self._type = 'Uploader'
        self._namespace = 'dpd_uploader'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'file_name', 'accepted_file_types', 'max_file_size', 'chunk_size', 'className', 'style', 'upload_in_progress', 'upload_complete', 'service']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Uploader, self).__init__(children=children, **args)
