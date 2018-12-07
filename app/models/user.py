from .. import bc
from .. import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    hash_global = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    size_screen = db.Column(db.String, nullable=False)
    os = db.Column(db.String, nullable=False)
    provider = db.Column(db.String, nullable=False)
    os_version = db.Column(db.String, nullable=False)
    browser = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password = bc.generate_password_hash(password)

    def verify_password(self, password):
        return bc.check_password_hash(self.password, password)
