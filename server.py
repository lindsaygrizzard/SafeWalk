from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, connect_to_db, db
from call import send_sms
from haversine import haversine

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

# on call --- enter route data
# not on call --- delete route data


@app.route("/match_walkers")
def match_walkers():

    """Filter on call users to match together based on proximity of origin and destination"""

    user_origin_lat = 5
    user_origin_lng = 4

    user_destination_lat = 5
    user_destination_lng = 4

    lat_range = .00724
    lng_range = .00943

    matches = []

    for other_user in route_table:
        if (other_user.origin_lat < user_origin_lat + lat_range and
            other_user.origin_lat > user_origin_lat - lat_range and
            other_user.origin_lng < user_origin_lng + lng_range and
            other_user.origin_lng > user_origin_lng - lng_range and
            other_user.destination_lat < user_destination_lat + lat_range and
            other_user.destination_lat > user_destination_lat - lat_range and
            other_user.destination_lng < user_destination_lng + lng_range and
            other_user.destination_lng > user_destination_lng - lng_range):
            # calculate distance using haversine and store dist and match id

            other_user_origin = (other_user.origin_lat, other_user.origin_lng)
            other_user_destination = (other_user.destination_lat, other_user.destination_lng)
            user_origin = (user_origin_lat, user_origin_lng)
            user_destination = (user_destination_lat, user_destination_lng)


            origin_difference = haversine(other_user_origin, user_origin)
            destination_difference = haversine(other_user_destination, user_destination)

            total = origin_difference + destination_difference
            matches.append((total, other_user_id))

    matches.sort()

    close_matches = []
    for i in range(4):
        user_id = matches[i][1]
        match_phone = query_for_match_phone
        match_name = query_for_match_name
        match_photo = query_for_match_photo
        close_matches.append((user_id, match_phone, match_name, match_photo))


    # query by match id (in order - lowest 5) - get contacts --> initialize twilio contact




##################################
    # Rate walking companion #
##################################

@app.route("/rating", methods=["POST", "GET"])
def rate_user():

    if request.method == "POST":
        user_email = session['email']
        user = User.query.filter_by(email=user_email).first()

        scored_user_id = request.form['scored_user_id']
        safety_score = request.form['safety']
        respect_score = request.form['respect']

        overall_rating = (0.7 * int(safety_score)) + (0.3 * int(respect_score))

        print overall_rating

        new_rating_entry = Rating(rating_user_id=user, 
                            scored_user_id=scored_user_id, 
                            overall_rating=int(overall_rating))

        db.session.add(new_rating_entry)
        db.session.commit() 

        return redirect("/")

    else:
        return render_template("rating.html")



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    connect_to_db(app)

    app.run()