from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key = True)
    email = db.Column(db.String(45), unique=True, index=True)
    name = db.Column(db.String(45), unique=True, index=True)
    password = db.Column(db.String(45), unique=True, index=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password