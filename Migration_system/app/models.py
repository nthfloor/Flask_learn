from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True, unique = True)
    lastname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<User %r>' % (self.firstname)
