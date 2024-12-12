# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    user_testing1.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/09 18:00:03 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/12 16:03:12 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, jsonify, request, url_for, redirect, render_template

test_user_bp = Blueprint('test_user', __name__, url_prefix='/test_user')

@test_user_bp.route('/hi', methods=['GET'])
def hi():
    return jsonify({"message": "Hi!"})

#cleaning the user database
@test_user_bp.route('/clean_database', methods=['GET'])
def clean_database():
    from models.user_model import execute_query
    execute_query("DELETE FROM users")
    return jsonify({"message": "Database cleaned."})
    

# Model testing

from models.user_model import get_user_by_id, get_user_by_username, create_user, update_user
from faker import Faker

fake = Faker()

# Create a new fake user

# @test_user_bp.route('/create_user', methods=['GET'])
# def test_create_user():
#     username = fake.user_name()
#     email = fake.email()
#     password_hash = fake.password()
#     birthdate = fake.date_of_birth()
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     user = create_user(username, email, password_hash, birthdate, first_name, last_name)
#     assert user["username"] == username
#     assert user["email"] == email
#     assert user["first_name"] == first_name
#     assert user["last_name"] == last_name
#     return jsonify(user)

@test_user_bp.route('/create_user', methods=['GET'])
def test_create_user():
    user = fake.simple_profile()
    username = user["username"]
    email = user["mail"]
    password_hash = "1234"
    birthdate = user["birthdate"]
    create_user(username, email, password_hash, birthdate)
    return jsonify({"message": "User created.", "username": username, "email": email, "birthdate": birthdate})
    

# Get a user by ID

# @test_user_bp.route('/get_user_by_id', methods=['GET'])
# def test_get_user_by_id():
#     user = create_user(fake.user_name(), fake.email(), fake.password(), fake.date_of_birth(), fake.first_name(), fake.last_name())
#     user_id = user["id"]
#     user = get_user_by_id(user_id)
#     assert user["id"] == user_id
#     return jsonify(user)

# form for seeig the user by id
@test_user_bp.route('/get_user_by_id_form', methods=['GET'])
def get_user_by_id_form():
    return """
    <form action="/test_user/get_user_by_id" method="get">
        <label for="user_id">User ID:</label><br>
        <input type="text" id="user_id" name="user_id"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/get_user_by_id', methods=['GET'])
def test_get_user_by_id():
    user_id = request.args.get("user_id")
    user = get_user_by_id(user_id)
    return jsonify(user)

# update user

# @test_user_bp.route('/update_user', methods=['GET'])
# def test_update_user():
#     user = create_user(fake.user_name(), fake.email(), fake.password(), fake.date_of_birth(), fake.first_name(), fake.last_name())
#     user_id = user["id"]
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     user = update_user(user_id, first_name=first_name, last_name=last_name)
#     assert user["first_name"] == first_name
#     assert user["last_name"] == last_name
#     return jsonify(user)

# form for updating the user
@test_user_bp.route('/update_user_form', methods=['GET'])
def update_user_form():
    return """
    <form action="/test_user/update_user" method="get">
        <label for="user_id">User ID:</label><br>
        <input type="text" id="user_id" name="user_id"><br>
        <label for="first_name">First Name:</label><br>
        <input type="text" id="first_name" name="first_name"><br>
        <label for="last_name">Last Name:</label><br>
        <input type="text" id="last_name" name="last_name"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/update_user', methods=['GET'])
def test_update_user():
    user_id = request.args.get("user_id")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    user = update_user(user_id, first_name=first_name, last_name=last_name)
    return jsonify(user)

from models.user_model import delete_user

# delete user
# @test_user_bp.route('/delete_user', methods=['GET'])
# def test_delete_user():
#     user = create_user(fake.user_name(), fake.email(), fake.password(), fake.date_of_birth(), fake.first_name(), fake.last_name())
#     user_id = user["id"]
#     user = delete_user(user_id)
#     assert get_user_by_id(user_id) is None
#     return jsonify({"message": "User deleted."})

# form for deleting the user
@test_user_bp.route('/delete_user_form', methods=['GET'])
def delete_user_form():
    return """
    <form action="/test_user/delete_user" method="get">
        <label for="user_id">User ID:</label><br>
        <input type="text" id="user_id" name="user_id"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/delete_user', methods=['GET'])
def test_delete_user():
    user_id = request.args.get("user_id")
    user = delete_user(user_id)
    return jsonify(user)

# get user by username
from models.user_model import get_user_by_username
@test_user_bp.route('/get_user_by_username', methods=['GET'])
def test_get_user_by_username():
    username = request.args.get("username")
    user = get_user_by_username(username)
    return jsonify(user)

@test_user_bp.route('/get_user_by_username_form', methods=['GET'])
def get_user_by_username_form():
    return """
    <form action="/test_user/get_user_by_username" method="get">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <input type="submit" value="Submit">
    </form>
    """

#manager testing

from manager.user_manager import get_user_details, update_user_profile, delete_user_account, register_user

# register user
# @test_user_bp.route('/register_user', methods=['GET'])
# def test_register_user():
#     username = " "
#     email = fake.email()
#     password = "12345678"
#     birthdate = fake.date_of_birth()
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     user = register_user({"username": username, "email": email, "password": password, "birthdate": birthdate, "first_name": first_name, "last_name": last_name})
#     return jsonify(user)
#     # def register_user(data: Dict) -> Dict:

# form for registering the user with username password and mail
@test_user_bp.route('/register_user_form', methods=['GET'])
def register_user_form():
    return """
    <form action="/test_user/register_user" method="get">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <label for="password">Password:</label><br>
        <input type="text" id="password" name="password"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/register_user', methods=['GET'])
def test_register_user():
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    user = register_user({"username": username, "email": email, "password": password})
    return jsonify(user)

#login user
from manager.user_manager import authenticate_user
@test_user_bp.route('/login_user', methods=['GET'])
def test_login_user():
    username = "recursivelover"
    password = "123456789"
    try:
        user = authenticate_user(username, password)
        return jsonify(user)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    user = authenticate_user(username, password)
    return jsonify(user)

# complete version of register user
# @test_user_bp.route('/register', methods=['GET'])
# def register_user_route():
#     return render_template('register_test.html')
    
# @test_user_bp.route('/register', methods=['POST'])
# def register_user_route_post():
#     data = request.form
#     try:
#         register_user(data)
#         return """
#         <h1>Success</h1>
#         """
#     except ValueError as e:
#         return render_template('register_test.html', error_message=str(e))
#     except Exception as e:
#         return render_template('register_test.html', error_message=f"Internal Server Error {str(e)}")

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_verification_token(email):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

@test_user_bp.route('/generate_verification_token_form', methods=['GET'])
def generate_verification_token_form():
    return """
    <form action="/test_user/generate_verification_token" method="get">
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/generate_verification_token', methods=['GET'])
def test_generate_verification_token():
    email = request.args.get("email")
    token = generate_verification_token(email)
    return jsonify({"token": token})

@test_user_bp.route('/check_verification_token_form', methods=['GET'])
def check_verification_token_form():
    return """
    <form action="/test_user/check_verification_token" method="get">
        <label for="token">Token:</label><br>
        <input type="text" id="token" name="token"><br>
        <input type="submit" value="Submit">
    </form>
    """

from itsdangerous import SignatureExpired, BadSignature

def check_verification_token(token):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        return email
    except SignatureExpired:
        return "The token is expired."
    except BadSignature:
        return "The token is invalid."

@test_user_bp.route('/check_verification_token', methods=['GET'])
def test_check_verification_token():
    token = request.args.get("token")
    email = check_verification_token(token)
    return jsonify({"email": email})

from models.user_model import validate_user

@test_user_bp.route('/verify/<token>', methods=['GET'])
def verify(token):
    email = check_verification_token(token)
    if email == "The token is expired.":
        return render_template('expired_token.html') # TODO: Crear template y  Añadir link para reenviar correo
    elif email == "The token is invalid.":
        return render_template('invalid_token.html') # TODO: Crear template
    else:
        validate_user(email)
        return render_template('verified_test.html')

def generate_verification_link(email):
    token = generate_verification_token(email)
    return url_for('test_user.verify', token=token, _external=True)

@test_user_bp.route('/generate_verification_link_form', methods=['GET'])
def generate_verification_link_form():
    return """
    <form action="/test_user/generate_verification_link" method="get">
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_user_bp.route('/generate_verification_link', methods=['GET'])
def test_generate_verification_link():
    email = request.args.get("email")
    link = generate_verification_link(email)
    return jsonify({"link": link})

# @test_user_bp.route('/check_verification_token', methods=['GET'])
# def test_check_verification_token():
#     token = request.args.get("token")
#     email = check_verification_token(token)
#     return jsonify({"email": email})


from flask import render_template, request, redirect, url_for, flash, jsonify
from faker import Faker

fake = Faker()

@test_user_bp.route('/register', methods=['GET'])
def register_user_route():
    return render_template('register_test.html')

from flask import current_app
from flask_mail import Message
import logging


def send_verification_email(username, email):
    logging.info(f"Sending verification email to {email}")
    # Generar enlace de verificación único
    link = generate_verification_link(email)

    # Configurar el correo electrónico
    msg = Message(
        subject="Verify your email",
        recipients=[email],
        html=render_template('verification_mail.html', username=username, verification_link=link, email=email)
    )
    mail = current_app.extensions['mail']
    mail.send(msg)

@test_user_bp.route('/register', methods=['POST'])
def register_user_route_post():
    data = request.form
    logging.info(f"Received registration data: {data}")
    try:
        register_user(data)
        logging.info(f"User {data['username']} registered successfully.")
        send_verification_email(data["username"], data["email"])
        logging.info(f"Verification email sent to {data['email']}")
        return render_template('registered_test.html')
    except ValueError as e:
        return render_template('register_test.html', error_message=str(e))
    except Exception as e:
        return render_template('register_test.html', error_message=f"Internal Server Error {str(e)}")

@test_user_bp.route('/generate_example_data', methods=['GET'])
def generate_example_data():
    example_data = {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password()
    }
    return jsonify(example_data)


@test_user_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login_test.html')