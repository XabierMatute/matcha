# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cookie_testing.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/19 12:03:41 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/19 17:16:04 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from logging import getLogger

logging = getLogger(__name__)


test_cookie_bp = Blueprint('test_cookie', __name__, url_prefix='/test_cookie')

def generate_login_cookie(user_id):
    """
    Generates a login cookie for the given user ID.

    Args:
        user_id (int): The ID of the user to generate the cookie for.

    Returns:
        str: The generated login cookie.
    """
    logging.debug(f"Generating login cookie for user ID: {user_id}")
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    cookie = serializer.dumps(user_id, salt=app.config['SECURITY_PASSWORD_SALT'])
    logging.debug(f"Generated cookie: {cookie}")
    return cookie

def get_user_by_cookie(cookie):
    """
    Retrieves the user ID from the given cookie.

    Args:
        cookie (str): The cookie to retrieve the user ID from.

    Returns:
        int: The user ID retrieved from the cookie.
    """
    logging.debug(f"Getting user ID from cookie: {cookie}")
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    user_id = serializer.loads(cookie, salt=app.config['SECURITY_PASSWORD_SALT'])
    logging.debug(f"Retrieved user ID: {user_id}")
    return user_id

from manager.user_manager import get_user_by_id

def get_username_by_cookie(cookie):
    """
    Retrieves the username from the given cookie.

    Args:
        cookie (str): The cookie to retrieve the username from.

    Returns:
        str: The username retrieved from the cookie.
    """
    logging.debug(f"Getting username from cookie: {cookie}")
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    id = serializer.loads(cookie, salt=app.config['SECURITY_PASSWORD_SALT'])
    user = get_user_by_id(id)
    if not user:
        logging.error(f"User not found for ID: {id}")
        return None
    username = user['username']
    logging.debug(f"Retrieved username: {username}")
    return username

@test_cookie_bp.route('/my_username')
def my_username():
    cookie = request.cookies.get('user')
    if not cookie:
        return jsonify({'error': 'No user cookie found, please log in'})
    username = get_username_by_cookie(cookie)
    return jsonify({'username': username})

@test_cookie_bp.route('/generate_cookie_user_form')
def generate_cookie_user_form():
    return """
    <form action="/generate_cookie_user" method="post">
        <label for="user_id">User ID:</label><br>
        <input type="text" id="user_id" name="user_id"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_cookie_bp.route('/generate_cookie_user', methods=['POST'])
def generate_cookie_user():
    user_id = request.form.get('user_id')
    cookie = generate_login_cookie(user_id)
    response = jsonify({'cookie': cookie})
    response.set_cookie('user', cookie)
    return response

@test_cookie_bp.route('/get_user_by_cookie_form')
def get_user_by_cookie_form():
    return """
    <form action="/get_user_by_cookie" method="post">
        <label for="cookie">Cookie:</label><br>
        <input type="text" id="cookie" name="cookie"><br>
        <input type="submit" value="Submit">
    </form>
    """

@test_cookie_bp.route('/get_user_by_cookie', methods=['POST'])
def get_user_by_cookie_route():
    cookie = request.form.get('cookie')
    user_id = get_user_by_cookie(cookie)
    return jsonify({'user_id': user_id})


@test_cookie_bp.route('/cookie')
def cookie():
    resp = jsonify({'message': 'Cookie set'})
    resp.set_cookie('gallete', 'pallete')
    resp.set_cookie('logged', 'true')
    resp.set_cookie('username', 'genaro')
    return resp

@test_cookie_bp.route('/print_cookie')
def print_cookie():
    return jsonify({'cookie': request.cookies})

@test_cookie_bp.route('/print_gallete')
def print_gallete():
    return jsonify({'gallete': request.cookies.get('gallete')})

@test_cookie_bp.route('/clear_cookie')
def clear_all_cookies():
    resp = jsonify({'message': 'All cookies cleared'})
    for cookie in request.cookies:
        resp.set_cookie(cookie, '', expires=0)
    return resp