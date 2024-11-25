from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms import EmailField
from flask_wtf.file import FileRequired, FileAllowed
from PIL import Image
import io
import psycopg  # Usamos psycopg3 en lugar de psycopg2
from app import app  # Para usar las configuraciones de la base de datos

# Conexión a la base de datos (se usa en las validaciones)
def get_db_connection():
    # Utilizando psycopg3 (psycopg) para la conexión con la base de datos
    conn = psycopg.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    return conn

class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        # Realizar la consulta directamente para verificar si el email ya está registrado
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email.data,))
            user = cursor.fetchone()
        conn.close()

        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

    def validate_username(self, username):
        # Realizar la consulta directamente para verificar si el username ya está tomado
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username.data,))
            user = cursor.fetchone()
        conn.close()

        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Allows the user to stay logged in
    submit = SubmitField('Login')

    def validate_username(self, username):
        # Validar que el usuario exista en la base de datos
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username.data,))
            user = cursor.fetchone()
        conn.close()

        if not user:
            raise ValidationError('No account found with that username.')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], validators=[DataRequired()])
    sexual_preferences = SelectField('Sexual Preferences', choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')], validators=[DataRequired()])
    submit = SubmitField('Update Profile')



