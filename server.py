from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, connect_to_db, db

app = Flask(__name__)
app.secret_key = 'public key'


@app.route('/')
def index():

    """Homepage."""

    if 'email' not in session:
        flash('You must Log In or Register before viewing projects')
        return redirect('/login')
    else:
        flash('Hello %s' % session['email'])
    return render_template('index.html')


##################################
    #SIGN UP/ LOGIN/ SIGN OUT
##################################


@app.route("/register")
def user_signup():

    """Sign up a new user."""

    return render_template("/register.html")


@app.route("/register-process", methods=['POST'])
def process_signup():

    """Route to process login for users."""

    entered_email = request.form['email']
    phone = request.form['phone']
    entered_pw = request.form['password']
    entered_pw2 = request.form['password2']

    print "entered_email", entered_email
    print "entered_pw", entered_pw
    print "entered_pw2", entered_pw2

    if User.query.filter(User.email == entered_email).first():
        flash("Hmm...we already have your email account on file. Please log in.")
        return redirect("/login")
    else:
        new_user = User(password=entered_pw, email=entered_email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

@app.route("/login")
def user_login():

    """Login page with form for users."""

    return render_template("login.html")


@app.route("/login-process", methods=['POST'])
def process_login():

    """Route to process login for users."""

    entered_email = request.form['email']
    entered_pw = request.form['password']

    user = User.query.filter_by(email=entered_email).first()

    if user:
        if entered_pw == user.password:
            session['email'] = request.form['email']
            return redirect("/")
        else:
            flash("That is not the correct password!")
            return redirect('/login')
    else:
        flash('That information was not found')
        return redirect('login')


@app.route("/logout")
def process_logout():

    """Route to process logout for users."""

    session.pop('user_id', None)
    session.pop('email', None)
    flash('You successfully logged out!')
    return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    connect_to_db(app)

    app.run()
