from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# FIX: Might need an Association table set up like this instead:
# # Association Table of Ratings and Users
rating_list = db.Table('rating_list',
    db.Column("rating_id", db.Integer, autoincrement=True, primary_key=True),
    db.Column('primary_user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('seconday_user_id', db.Integer, db.ForeignKey('users.user_id'))
)

class User(db.Model):
    """Table of users"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<User user_id:  %s | email: %s>" % (self.user_id, self.email)

    @property
    def rating_avg(self):
        rating_sum = 0
        for rating in self.ratings:
            rating_sum += rating.score

        rating_avg = rating_sum / len(self.ratings)
        
        return rating_avg

class Route(db.Model):
    """Table of routes"""

    __tablename__ = "routes"

    route_id =  db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)


# class Rating(db.Model):
#     """Table of ratings"""

#     __tablename__ = "ratings"

#     rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     rating_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     scored_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer)

#     user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

#     def __repr__(self):

#         """Provide helpful representation when printed"""

#         return "<Rating rating_id:  %s >" % (self.rating_id)


#############################
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empowerwalk.db'
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

def seed_users():
    l = User(email = 'lindsay@gmail.com',
            password = 'abc',
            phone = '+16617946615',
            zipcode='94110')
    db.session.add(l)

    n = User(email = 'natalie@gmail.com',
            password = 'abc',
            phone = '+14157024046',
            zipcode='94110')

    db.session.add(n)
    db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
    #seed_users()
    #print "Seeded 2 beta users."