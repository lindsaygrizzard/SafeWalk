from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import pagerduty as pg
import json

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined





@app.route('/')
def index():

    """Homepage."""

    print "TEST!"
    
    return render_template("index.html")







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
