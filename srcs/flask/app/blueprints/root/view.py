# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    view.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 12:36:41 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 12:54:01 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import current_app
from config import DEBUG
from utils.list_routes import list_routes

def view():
    if not DEBUG:
        return "<p>Work in progress</p>"
        # TODO: there should be a redirect to the login/home page
    else:
        return "<h1>Welcome to Matcha! <3</h1>" + list_routes(current_app)