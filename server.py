from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
import json

app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined





@app.route('/')
def index():

    """Homepage."""

    print "TEST!"
    response = requests.get(
    "https://apitester.pagerduty.com/api/v1/users",
    headers = {
        "Authorization": "Token token=jvTJtbBKEPADtZyKyhrr",
    },
    verify = True,  # Verify SSL certificate
    )

    #Here is the info one can get about users, info can also be inserted
    #alerts can also be found and inserted
    users = response.json()['users']
    print "USERS OBJECTS IN LIST: ", users

    return render_template("index.html", users=users)







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
