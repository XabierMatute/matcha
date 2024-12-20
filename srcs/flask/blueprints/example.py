# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    example.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/20 15:32:20 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 16:51:12 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, render_template

example_bp = Blueprint('example', __name__)

@example_bp.route('/example')
def example():
    return render_template('example.html')


# esto seguramente no bva aqui

from utils.list_routes import list_routes as list_routex
from flask import current_app as app

@example_bp.route("/")
def list_routes():
    return render_template('content.html', content=list_routex(app))

from flask import redirect, url_for

@example_bp.route("/register")
def register():
    return redirect('users/register')

@example_bp.route("/login")
def login():
    if session.get('logged_in'):
        return redirect('users/account/' + session.get('username'))
    return redirect('users/login')

@example_bp.route("/logout")
def logout():
    return redirect('users/logout')

from flask import session

@example_bp.route("/account")
def account():
    if session.get('logged_in'):
        return redirect('users/account/' + session.get('username'))
    else:
        return redirect('users/login')

@example_bp.route('/users/details?user_id=1')
def fake():
    json = {
        "success": True,
        "message": "User details fetched successfully.",
        "data": {"id": 1, "username": "testuser", "email": "test@example.com"}
    }
    return json