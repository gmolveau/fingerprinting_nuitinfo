from .. import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    hash_global = db.Column(db.String, nullable=False)
    hash_language = db.Column(db.String, nullable=False)
    hash_gps = db.Column(db.String, nullable=False)
    hash_size_screen = db.Column(db.String, nullable=False)
    hash_os = db.Column(db.String, nullable=False)
    hash_provider = db.Column(db.String, nullable=False)
    hash_os_version = db.Column(db.String, nullable=False)
    hash_browser = db.Column(db.String, nullable=False)


