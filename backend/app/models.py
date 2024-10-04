from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db  # Ensure that db is already initialized here

# User model representing each user in the application
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(10))  # e.g., Male, Female, Other
    sexual_preferences = db.Column(db.String(50))  # e.g., Heterosexual, Homosexual, Bisexual
    biography = db.Column(db.Text)
    fame_rating = db.Column(db.Float, default=0.0)  # Define your fame rating logic
    profile_picture = db.Column(db.String(200))  # URL or path to profile picture
    location = db.Column(db.String(100))  # Store location as a string (e.g., neighborhood)
    latitude = db.Column(db.Float)  # For GPS coordinates
    longitude = db.Column(db.Float)  # For GPS coordinates
    is_active = db.Column(db.Boolean, default=False)
    # Updated relationship to allow many-to-many with interests
    interests = db.relationship('Interest', secondary='user_interests', lazy='subquery',
                                backref=db.backref('users', lazy=True))
    pictures = db.relationship('Picture', backref='user', lazy=True)
    viewed_profiles = db.relationship('ProfileView', backref='viewer', lazy=True)
    liked_profiles = db.relationship('Like', backref='liker', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Many-to-many relationship for interests
user_interests = db.Table('user_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
)

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True, nullable=False)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ProfileView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    liked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Chat {self.id}: {self.message[:20]}>'







