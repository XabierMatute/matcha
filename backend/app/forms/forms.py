from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms import EmailField
from app.models import User  # Asegúrate de que User esté correctamente definido aquí
from flask_wtf.file import FileRequired, FileAllowed
from PIL import Image
import io

# Aquí van las definiciones de RegistrationForm, LoginForm y ProfileForm


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Validation to ensure the email is unique
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

    # Validation to ensure the username is unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Allows the user to stay logged in
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], validators=[DataRequired()])
    sexual_preferences = SelectField('Sexual Preferences', choices=[('M', 'Men'), ('F', 'Women'), ('B', 'Both')], validators=[DataRequired()])
    
    # Set maximum length for biography (200 words)
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(max=1200)])  # 200 words ~ 1200 characters
    
    interests = StringField('Interests (e.g. #vegan, #geek)', validators=[DataRequired(), Length(max=100)])
    
    # Image file upload with validation
    profile_picture = FileField('Profile Picture', validators=[
        FileRequired('File was empty!'),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    
    submit = SubmitField('Save')

    # Custom validation for interests (example)
    def validate_interests(self, interests):
        if not all(tag.startswith('#') for tag in interests.data.split()):
            raise ValidationError('All interests must start with a "#" (e.g. #vegan, #geek).')

    # Custom validation for image dimensions
    def validate_profile_picture(self, profile_picture):
        img_data = profile_picture.data.stream.read()  # Read the file stream
        image = Image.open(io.BytesIO(img_data))  # Open the image using Pillow
        
        # Check dimensions
        if image.width > 800 or image.height > 800:
            raise ValidationError('Image dimensions must not exceed 800x800 pixels.')
