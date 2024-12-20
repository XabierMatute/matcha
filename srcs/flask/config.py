# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:45 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 10:48:54 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

DEBUG = True

class SecretConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SASECURITY_PASSWORD_SALTLT = os.getenv('SECURITY_PASSWORD_SALT')
    config = {'SECRET_KEY': SECRET_KEY, 'SECURITY_PASSWORD_SALT': SASECURITY_PASSWORD_SALTLT}

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

class UserConfig:
    DEBUG = DEBUG
    TESTING = True
    USERNAME_MIN_LENGTH = 3 # TODO: Añadir max_length
    PASSWORD_MIN_LENGTH = 3

class MailConfig:
    DEBUG = DEBUG
    ACTIVE = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    config = {'MAIL_SERVER': MAIL_SERVER, 'MAIL_PORT': MAIL_PORT, 'MAIL_USE_TLS': MAIL_USE_TLS, 'MAIL_USERNAME': MAIL_USERNAME, 'MAIL_PASSWORD': MAIL_PASSWORD, 'MAIL_DEFAULT_SENDER': MAIL_DEFAULT_SENDER}

class CookieConfig:
    DEBUG = DEBUG
    TESTING = True