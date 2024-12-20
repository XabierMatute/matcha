# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    example.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/20 15:32:20 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 15:33:01 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint, render_template

example_bp = Blueprint('example', __name__)

@example_bp.route('/example')
def example():
    return render_template('example.html')