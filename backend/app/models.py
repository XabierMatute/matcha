from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db  # Asegúrate de que db ya esté inicializado aquí

# Modelo de User que representa a cada usuario en la aplicación
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
    fame_rating = db.Column(db.Float, default=0.0)  # Lógica de fama
    profile_picture = db.Column(db.String(200))  # URL o ruta a la foto de perfil
    location = db.Column(db.String(100))  # Almacenar ubicación como string (e.g., vecindario)
    latitude = db.Column(db.Float)  # Coordenadas GPS
    longitude = db.Column(db.Float)  # Coordenadas GPS
    is_active = db.Column(db.Boolean, default=False)
    
    # Relación many-to-many para intereses
    interests = db.relationship('Interest', secondary='user_interests', lazy='subquery',
                                backref=db.backref('users', lazy=True))
    pictures = db.relationship('Picture', backref='user', lazy=True)

    # Especificar claves foráneas para evitar ambigüedades
    viewed_profiles = db.relationship('ProfileView', 
                                       foreign_keys='ProfileView.user_id',  # Quien está viendo
                                       backref='viewer', 
                                       lazy=True)
    viewed_users = db.relationship('ProfileView', 
                                    foreign_keys='ProfileView.viewed_user_id',  # Quien está siendo visto
                                    backref='viewed', 
                                    lazy=True)
    liked_profiles = db.relationship('Like', 
                                      foreign_keys='Like.user_id', 
                                      backref='liker', 
                                      lazy=True)
    liked_by_profiles = db.relationship('Like', 
                                         foreign_keys='Like.liked_user_id', 
                                         backref='liked_user', 
                                         lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Relación many-to-many para intereses
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Quien está viendo
    viewed_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Quien está siendo visto
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









