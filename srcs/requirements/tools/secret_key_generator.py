# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    secret_key_generator.py                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/12 12:19:00 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/12 12:26:00 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import secrets

# Generar una SECRET_KEY segura
SECRET_KEY = secrets.token_urlsafe()

print(SECRET_KEY)