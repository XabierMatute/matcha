# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:45 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/12 15:27:44 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# import os

# DEBUG = True

# class SecretConfig:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Valor por defecto si no está en .env
#     SASECURITY_PASSWORD_SALTLT = os.getenv('SECURITY_PASSWORD_SALT', 'default_salt')
#     config = {'SECRET_KEY': SECRET_KEY, 'SECURITY_PASSWORD_SALT': SASECURITY_PASSWORD_SALTLT}

# class RunConfig:
#     HOST = '0.0.0.0'
#     PORT = 5000
#     DEBUG = DEBUG

# class DatabaseConfig:
#     POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')  # Valor por defecto si no está en .env
#     POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
#     POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
#     POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')  # Valor por defecto si no está en .env
#     DEBUG = DEBUG

# class UserConfig:
#     DEBUG = DEBUG
#     TESTING = True
#     USERNAME_MIN_LENGTH = 3
#     PASSWORD_MIN_LENGTH = 3

# class MailConfig:
#     DEBUG = DEBUG
#     ACTIVE = True
#     MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.default.com')
#     MAIL_PORT = os.getenv('MAIL_PORT', '587')
#     MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True')
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default_email')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'default_password')
#     MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender')
#     config = {
#         'MAIL_SERVER': MAIL_SERVER,
#         'MAIL_PORT': MAIL_PORT,
#         'MAIL_USE_TLS': MAIL_USE_TLS,
#         'MAIL_USERNAME': MAIL_USERNAME,
#         'MAIL_PASSWORD': MAIL_PASSWORD,
#         'MAIL_DEFAULT_SENDER': MAIL_DEFAULT_SENDER
#     }
import os

DEBUG = True

class SecretConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Valor por defecto si no está en .env
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'default_salt')  # Corregido typo
    config = {'SECRET_KEY': SECRET_KEY, 'SECURITY_PASSWORD_SALT': SECURITY_PASSWORD_SALT}

class RunConfig:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = DEBUG

class DatabaseConfig:
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')  # Incluye el puerto
    DEBUG = DEBUG

class UserConfig:
    DEBUG = DEBUG
    TESTING = True
    USERNAME_MIN_LENGTH = 3
    PASSWORD_MIN_LENGTH = 3

class MailConfig:
    DEBUG = DEBUG
    ACTIVE = True
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.default.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))  # Asegura que sea int
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Convierte a booleano
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default_email')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'default_password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender')
    config = {
        'MAIL_SERVER': MAIL_SERVER,
        'MAIL_PORT': MAIL_PORT,
        'MAIL_USE_TLS': MAIL_USE_TLS,
        'MAIL_USERNAME': MAIL_USERNAME,
        'MAIL_PASSWORD': MAIL_PASSWORD,
        'MAIL_DEFAULT_SENDER': MAIL_DEFAULT_SENDER
    }
