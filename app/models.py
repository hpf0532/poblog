from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        return 'https://s.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username = username).first() == None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username = new_username).first() == None:
                break
            version += 1
        return new_username

    def __repr__(self):
        return '<User %r>' % (self.username)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
