from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
            rating_sum += rating

        return rating_sum / len(self.ratings)


class Rating(db.Model):
    """Table of ratings"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rating_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rated_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):

        """Provide helpful representation when printed"""

        return "<Rating rating_id:  %s >" % (self.rating_id)

#############################
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empowerwalk.db   '
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."

