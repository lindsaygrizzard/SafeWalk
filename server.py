from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Route
from call import send_sms
from haversine import haversine
from call import send_sms
import call

app = Flask(__name__)
app.secret_key = 'public key'


@app.route('/')
def index():

    """Homepage."""

    if 'email' not in session:
        flash('You must Log In or Register before viewing projects')
        return redirect('/login')

    return render_template('index.html')


@app.route('/call', methods=["POST"])
def call():
    """Make twilio call"""

    # query for the chosen other user
    send_sms()
    return "Success"



###########
#how do I make another route that will activate call.py on the index page?
###########

##################################
    #SIGN UP/ LOGIN/ SIGN OUT
##################################


@app.route("/register")
def user_signup():

    """Sign up a new user."""

    print "SESSION: ", session
    return render_template("/register.html")


@app.route("/register-process", methods=["POST"])
def process_signup():

    """Route to process login for users."""

    email = request.form['email']
    phone = request.form['phone']
    entered_pw = request.form['password']
    entered_pw2 = request.form['password2']

    if User.query.filter_by(email=email).first():
        flash("A user already exists with this email")
        return render_template("register.html")
    else:
        new_user = User(password=entered_pw, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        if not session.get('new_user.email'):
            session['email'] = new_user.email
        flash("You have been registered successfully.")
        return redirect("/")


@app.route("/login")
def user_login():

    """Login page with form for users."""

    return render_template("login.html")


@app.route("/process_login", methods=["POST"])
def process_login():
    """GET - displays a form that asks for email and password
        POST - collects that data and authenticates --> redirect to user profile"""

    email = request.form["email"]
    print "Email: ", email
    password = request.form["password"]
    user_object = User.query.filter(User.email == email).first()
    print "USER OBECT", user_object

    if user_object:
        if user_object.password == password:
            session["email"] = email
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


@app.route("/register_location", methods = ["POST"])
def register_route():

    """Add user's origin and destination to Route table"""
    print request.form
    originlat = request.form["marker1[latitude]"]
    originlng = request.form["marker1[longitude]"]
    destinationlat = request.form["marker2[latitude]"]
    destinationlng = request.form["marker2[longitude]"]

    print "here"
    user_obj = User.query.filter(User.email == session['email']).first()
    user_id = user_obj.user_id

    user_route = Route(route_user_id = user_id,
                        start_lat = originlat,
                        start_long = originlng,
                        end_lat = destinationlat,
                        end_long = destinationlng)

    db.session.add(user_route)
    db.session.commit()
   
    return redirect("/match_walkers")


# not on call --- delete route data


@app.route("/match_walkers", methods = ["POST"])
def match_walkers():

    """Filter on call users to match together based on proximity of origin and destination"""

    user_obj = User.query.filter(User.email == session['email']).first()
    user_route = user_obj.routes
    user_route = user_route[0]
    print "user route ", user_route
    
    user_origin_lat = user_route.start_lat
    user_origin_lng = user_route.start_long

    user_destination_lat = user_route.end_lat
    user_destination_lng = user_route.end_long

    lat_range = .00724
    lng_range = .00943

    matches = []

    other_users = Route.query.all()
    print "other user routes ", other_users

    for other_user in other_users:
        if other_user.route_user_id != user_obj.user_id:
            if (other_user.start_lat < user_origin_lat + lat_range and
                other_user.start_lat > user_origin_lat - lat_range and
                other_user.start_long < user_origin_lng + lng_range and
                other_user.start_long > user_origin_lng - lng_range and
                other_user.end_lat < user_destination_lat + lat_range and
                other_user.end_lat > user_destination_lat - lat_range and
                other_user.end_long < user_destination_lng + lng_range and
                other_user.end_long > user_destination_lng - lng_range):
                # calculate distance using haversine and store dist and match id

                other_user_origin = (other_user.start_lat, other_user.start_long)
                other_user_destination = (other_user.end_lat, other_user.end_long)
                user_origin = (user_origin_lat, user_origin_lng)
                user_destination = (user_destination_lat, user_destination_lng)


                origin_difference = haversine(other_user_origin, user_origin)
                destination_difference = haversine(other_user_destination, user_destination)

                total = origin_difference + destination_difference
                matches.append((total, other_user.route_user_id))
        else:
            print "no matches"

    if matches:
        matches.sort()
        print matches

        close_matches = []
        for i in range(4):
            user_id = matches[i][1]
            user_obj = User.query.get(user_id).first()
            a = user_obj.__dict__
            if '_sa_instance_state' in a:
                a.pop('_sa_instance_state')
            close_matches.append(a)

    return close_matches


    # query by match id (in order - lowest 5) - get contacts --> initialize twilio contact



##################################
    # Finish Walk #
##################################
@app.route("/finish", methods=['GET'])
def finish_walk():
    """After the user finishes her walk, take her to the rating form"""


    return redirect("/rating")

##################################
    # Rate walking companion #
##################################

@app.route("/rating", methods=["POST", "GET"])
def rate_user():

    if request.method == "POST":
        user_email = session['email']
        user = User.query.filter_by(email=user_email).first()

        scored_user_id = request.form['scored_user_id']
        scored_user_id = request.form['scored_user_id']
        scored_user = User.query.get(int(scored_user_id))
        safety_score = request.form['safety']
        respect_score = request.form['respect']

        overall_rating = (0.7 * int(safety_score)) + (0.3 * int(respect_score))

        print overall_rating

        # article = Article.query.filter_by(title=title).first()
        # for tag_name in tags:
        #     print tag_name
        #     tag = Tag.query.filter_by(tag_name=tag_name).first()
        #     article.tag_list.append(tag)

        # db.session.commit()
        scored_user.set_rating(overall_rating)
        db.session.commit()

        return redirect("/")

    else:
        return render_template("rating.html")

##################################
    # Invite a Friend #
##################################
@app.route("/invite", methods=['GET'])
def invite_friend():
    """Invite a friend to the app"""
    
    return render_template("invite.html")

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    connect_to_db(app)

    app.run()
