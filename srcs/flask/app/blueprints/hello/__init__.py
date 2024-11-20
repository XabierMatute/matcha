# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:50:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 12:59:37 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint

bp = Blueprint('hello', __name__, url_prefix="/hello")

@bp.route("")
def hola():
    return "<p>Aupa Pallete!</p>"