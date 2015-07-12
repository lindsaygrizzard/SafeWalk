from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, connect_to_db, db
from call import send_sms

app = Flask(__name__)
app.secret_key = 'public key'


@app.route('/')
def index():

    """Homepage."""

    # if 'email' not in session:
    #     flash('You must Log In or Register before viewing projects')
    #     return redirect('/login')
    # else:
    #     flash('Hello %s' % session['email'])

    
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


@app.route("/process_login", methods=["POST", "GET"])
def process_login():
    """GET - displays a form that asks for email and password
        POST - collects that data and authenticates --> redirect to user profile"""

    if request.method == "POST":
        email = request.form["email"]
        print "Email: ", email
        password = request.form["password"]
        user_object = User.query.filter(User.email == email).first()
        print "USER OBECT", user_object

        if user_object:
            if user_object.password == password:
                session["email"] = email
                flash("You logged in successfully")
                return redirect("/")
            else:
                flash("Incorrect password. Try again.")
                return redirect("/login")
        else:
            flash("We do not have this email on file. Click Register if you would like to create an account.")
            return redirect("/login")

    return render_template("login.html")
        ###


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
