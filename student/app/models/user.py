import uuid
from app.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    student_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:6])
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(15), nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.student_id:
            self.student_id = str(uuid.uuid4())[:7].upper()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'