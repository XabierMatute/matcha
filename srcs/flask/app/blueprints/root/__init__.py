# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:50:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 12:59:24 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint
from .view import view

bp = Blueprint('root', __name__, url_prefix="/")

@bp.route("/")
def root():
    return view()
    