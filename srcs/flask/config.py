# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:45 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/21 12:23:16 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

DEBUG = True

class SecretConfig:
    ACTIVE = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Valor por defecto si no está en .env
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'default_salt')  # Corregido typo
    config = {'SECRET_KEY': SECRET_KEY, 'SECURITY_PASSWORD_SALT': SECURITY_PASSWORD_SALT}

class RunConfig:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = DEBUG

class DatabaseConfig:
    ACTIVE = True
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')  # Incluye el puerto
    DEBUG = DEBUG

class UserConfig:
    DEBUG = DEBUG
    ACTIVE = True
    TESTING = False
    USERNAME_MIN_LENGTH = 3
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

class BlueprintConfig:
    DEBUG = DEBUG
    USERS = True
    LIKES = True
    NOTIFICATIONS = True
    INTERESTS = True
    CHAT = True
    PROFILE = True
    PICTURES = True
    EXAMPLE = True
    CUSTOM_ERRORS = True
    USER_TESTING = True
    COOKIE_TESTING = True
