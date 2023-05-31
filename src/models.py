from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # children = db.relationship('Favorites', backref='parent')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=True)
    # children = db.relationship('Favorites', backref='parent')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    # children = db.relationship('Favorites', backref='parent')

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planets_id = db.Column(
        db.Integer, db.ForeignKey('planets.id'), nullable=True)
    people_id = db.Column(
        db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets = db.relationship('Planets')
    people = db.relationship('People')
    user = db.relationship('User', backref='favorites')

    def __repr__(self):
        return 'Favorite %r' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.email,
            "planet_name": self.planets.name,
            "people_id": self.people.name

        }
