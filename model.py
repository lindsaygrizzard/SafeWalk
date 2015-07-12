from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Table of users"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    rating = db.Column(db.Integer, default=5)
    walk_count = db.Column(db.Integer, default=0)

    def get_walk_count(self):
 
        return self.walk_count

    def set_walk_count(self):
        self.walk_count += 1
        db.session.commit()
    
    def get_rating(self):
        return self.rating

    def set_rating(self, new_score):        
        """Sets new rating based on cummulative average"""
        
        old_average = self.get_rating() * self.get_walk_count()
        self.set_walk_count() # establish new walk is completed

        new_total = old_average + new_score
        new_rating = new_total / self.get_walk_count()
        self.rating = new_rating
        db.session.commit()

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<User user_id:  %s | email: %s>" % (self.user_id, self.email)

class Route(db.Model):
    """Table of routes"""

    __tablename__ = "routes"

    route_id =  db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)

    user = db.relationship("User", backref = db.backref("routes"))

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<Route route_id:  %s | user_id: %s>" % (self.route_id, self.route_user_id)

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
            phone = '+16617946615')
    db.session.add(l)

    n = User(email = 'natalie@gmail.com',
            password = 'abc',
            phone = '+14157024046')
    db.session.add(n)

    db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
    print "Created all tables"
    seed_users()
    print "Seeded 2 beta users."
    u = User.query.get(1)
    print "u references User 1"
