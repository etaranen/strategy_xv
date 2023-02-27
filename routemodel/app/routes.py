from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Graph MSXV Telemetry Data',
        description='Fetches telemetry data and graphs it',
        template='home-template',
        body="This is a homepage served with Flask."
    )