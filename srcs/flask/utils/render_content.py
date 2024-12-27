# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    render_content.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/27 17:33:19 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/27 17:33:47 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import render_template

def render_content(message):
    """Helper function to render content.html with a message."""
    return render_template('content.html', content=message)
