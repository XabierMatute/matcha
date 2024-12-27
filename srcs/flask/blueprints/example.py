# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    example.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/20 15:32:20 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 14:13:09 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, render_template

example_bp = Blueprint('example', __name__)

@example_bp.route('/example')
def example():
    return render_template('example.html')


# esto seguramente no bva aqui


# from flask import redirect, url_for

# @example_bp.route("/register")
# def register():
#     return redirect('users/register')

# @example_bp.route("/login")
# def login():
#     if session.get('logged_in'):
#         return redirect('users/account/' + session.get('username'))
#     return redirect('users/login')

# @example_bp.route("/logout")
# def logout():
#     return redirect('users/logout')

# from flask import session

# @example_bp.route("/account")
# def account():
#     if session.get('logged_in'):
#         return redirect('users/account/' + session.get('username'))
#     else:
#         return redirect('users/login')

# @example_bp.route('/users/details?user_id=1')
# def fake():
#     json = {
#         "success": True,
#         "message": "User details fetched successfully.",
#         "data": {"id": 1, "username": "testuser", "email": "test@example.com"}
#     }
#     return json