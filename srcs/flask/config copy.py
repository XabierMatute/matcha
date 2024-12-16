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

# Configuración para ejecutar la aplicación
class RunConfig:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = DEBUG

# Configuración de la base de datos
class DatabaseConfig:
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DEBUG = DEBUG

# Configuración para Flask-Mail
class MailConfig:
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Servidor de correo
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Puerto del servidor
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']  # Seguridad
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your_email@gmail.com')  # Email de envío
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_password')  # Contraseña
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'your_email@gmail.com')  # Remitente predeterminado

# Configuración global que combina todas las configuraciones
class Config(RunConfig, DatabaseConfig, MailConfig):
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Clave secreta para tokens y seguridad


# import os

# DEBUG = True  # Modo de depuración activado por defecto

# class RunConfig:
#     """Configuración para ejecutar la aplicación."""
#     HOST = os.getenv('APP_HOST', '0.0.0.0')  # Permite configuración dinámica
#     PORT = int(os.getenv('APP_PORT', 5000))  # Valor predeterminado: 5000
#     DEBUG = DEBUG

# class DatabaseConfig:
#     """Configuración para la base de datos."""
#     POSTGRES_DB = os.getenv('POSTGRES_DB')
#     POSTGRES_USER = os.getenv('POSTGRES_USER')
#     POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
#     POSTGRES_HOST = os.getenv('POSTGRES_HOST')
#     DEBUG = DEBUG

#     @staticmethod
#     def validate():
#         """Valida que todas las variables necesarias estén configuradas."""
#         required_vars = ['POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST']
#         for var in required_vars:
#             if not os.getenv(var):
#                 raise ValueError(f"Environment variable {var} is required but not set.")
