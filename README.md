# django-plotly-dash-uploader

dash-uploader is a Django Dash component library.

This component enables uploading of any fie size so files of any size can be uploaded to your app, using the [ResumableJS](http://resumablejs.com/) library. 

It was also made to be compatible with the [django-plotly-dash](https://github.com/GibbsConsulting/django-plotly-dash) extension of the Dash Library.

*NOTE:* The uploading does not take advantage of Django's MEDIAL url, uploading, fields, and forms. I specifically needed to make it for uploading User 'csv' and 'excel' files as a quick fix.

## Usage

### 1. Enable Collect Static Files for Component
Make sure to add this library to the list in the Django Plolty Dash setting like below 

```
PLOTLY_COMPONENTS = [
    <other added compoenets>
     ...,
    'dpd_uploader',
]
```

### 2. Init the `dpd_uploader` Component
Where you need it in you app add the component like below.

The actual HTML element is just a `div` the the ResumableJS callback on it. You can add any children you want to as needed.

```Python
import dash_html_components as html
import dash_bootstrap_components as dbc
import dpd_uploader as du

UPLOAD_API_ENDPOINT = '<REST API for ResumableJS POST callback>'

component = du.Uploader(
    id=UPLOAD_BUTTON_ID,
    service=UPLOAD_API_ENDPOINT,
    children=dbc.Button(
        block=True,
        size="lg",
        style=UPLOAD_BUTTON_CSS,
        color="primary",
        children=html.Span(id=UPLOAD_BUTTON_TEXT_SPAN_ID,
                            children="Click or drag file here to Upload."),
    ),
)
```

Other useful **props** for this component can be found and documented in this [file](https://github.com/alexwolf22/dpd-uploader/blob/master/dpd_uploader/Uploader.py).

### 3. Create the Django POST view to handle Data Uploading
Since this library just has the component it is up to you to build the view to handle the upload.

I have shared the one I made in this repo which you can use as a reference found [here](./example_django_post_view.py). My code requires *python3*.
You will need to set up the proper URL in Django pasted off the `UPLOAD_BUTTON_ID` you set above.

**NOTE**: I only made the POST request from ResumableJS. This repo can be modified to enable uploads to be resumed after browser restarts by created a GET request in this React Component along with the Django view handling it. 

### 4. Make the callback to handle the file uploading
The callback if the file uplaod was completed with set the prop complated to `True`, and the `file_name` prop would be the name of the file which was uploaded.

How every you configure your view to store your file you will need to find the correct path to on it your host machine.

The callback can look something like this

```python
@app.expanded_callback(
    output=[
        Output(<OUPUT_ID>, <OUTPUT_PROP>)
    ],
    inputs=[
        Input(UPLOAD_BUTTON_ID, "upload_complete"),
        Input(UPLOAD_BUTTON_ID, "file_name"),
    ]
)
def handle_data_upload(upload_completed: bool,
                       file_name: Optional[str],
                       user: User,
                       session_state: Dict,
                       **_kwargs: Dict) -> List:

    # Get path file uploaded to with ResumableJS in Upload component
    if not upload_completed or not file_name:
        return [False, '', '', '']

    # The full file path needs to be programmatically set based on 
    # how you handle it in your view
    file_path = f'/tmp/file_uploads/{file_name}'
    
    # Handle the filepath as needed
```



# Working with the codebase
Get started with:
1. Install Dash and its dependencies: https://dash.plotly.com/installation
2. Run `python usage.py`
3. Visit http://localhost:8050 in your web browser

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

### Install dependencies

If you have selected install_dependencies during the prompt, you can skip this part.

1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.
    ```
    $ virtualenv venv
    $ . venv/bin/activate
    ```
    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```

### Write your component code in `src/lib/components/Uploader.react.js`.

- The demo app is in `src/demo` and you will import your example component code into your demo app.
- Test your code in a Python environment:
    1. Build your code
        ```
        $ npm run build
        ```
    2. Run and modify the `usage.py` sample dash app:
        ```
        $ python usage.py
        ```
- Write tests for your component.
    - A sample test is available in `tests/test_usage.py`, it will load `usage.py` and you can then automate interactions with selenium.
    - Run the tests with `$ pytest tests`.
    - The Dash team uses these types of integration tests extensively. Browse the Dash component code on GitHub for more examples of testing (e.g. https://github.com/plotly/dash-core-components)
- Add custom styles to your component by putting your custom CSS files into your distribution folder (`dpd_uploader`).
    - Make sure that they are referenced in `MANIFEST.in` so that they get properly included when you're ready to publish your component.
    - Make sure the stylesheets are added to the `_css_dist` dict in `dpd_uploader/__init__.py` so dash will serve them automatically when the component suite is requested.
- [Review your code](./review_checklist.md)

### Create a production build and publish:

1. Build your code:
    ```
    $ npm run build
    ```
2. Create a Python distribution
    ```
    $ python setup.py sdist bdist_wheel
    ```
    This will create source and wheel distribution in the generated the `dist/` folder.
    See [PyPA](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project)
    for more information.

3. Test your tarball by copying it into a new environment and installing it locally:
    ```
    $ pip install dpd_uploader-0.0.1.tar.gz
    ```

4. If it works, then you can publish the component to NPM and PyPI:
    1. Publish on PyPI
        ```
        $ twine upload dist/*
        ```
    2. Cleanup the dist folder (optional)
        ```
        $ rm -rf dist
        ```
    3. Publish on NPM (Optional if chosen False in `publish_on_npm`)
        ```
        $ npm publish
        ```
        _Publishing your component to NPM will make the JavaScript bundles available on the unpkg CDN. By default, Dash serves the component library's CSS and JS locally, but if you choose to publish the package to NPM you can set `serve_locally` to `False` and you may see faster load times._

5. Share your component with the community! https://community.plotly.com/c/dash
    1. Publish this repository to GitHub
    2. Tag your GitHub repository with the plotly-dash tag so that it appears here: https://github.com/topics/plotly-dash
    3. Create a post in the Dash community forum: https://community.plotly.com/c/dash
