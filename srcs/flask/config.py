# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:45 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/02 14:27:44 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

DEBUG = True

class RunConfig:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = DEBUG

class DatabaseConfig:
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    DEBUG = DEBUG

