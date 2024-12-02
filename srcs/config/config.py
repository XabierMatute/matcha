# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:26:45 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 12:30:38 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# import os

# DEBUG = True

# class RunConfig:
#     HOST = '0.0.0.0'
#     PORT = 5000
#     DEBUG = DEBUG
import os

class Config:
    """Configuración base común para todos los entornos"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Clave secreta
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'default_salt')  # Salt para tokens seguros
    DEBUG = False
    TESTING = False

    # Configuración de la base de datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/default_db')

    # Configuración de correo
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Correo del remitente
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Contraseña generada
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # Correo por defecto como remitente

    # Otras configuraciones globales
    SESSION_COOKIE_SECURE = True  # Cookies seguras
    JSON_SORT_KEYS = False        # No ordenar claves JSON automáticamente
    PERMANENT_SESSION_LIFETIME = 3600  # Duración de las sesiones (segundos)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    MAIL_DEBUG = True  # Activa depuración de correos
    SESSION_COOKIE_SECURE = False  # Cookies no seguras en desarrollo

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    MAIL_DEBUG = True  # Activa depuración de correos
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/test_db')
    SESSION_COOKIE_SECURE = False  # Cookies no seguras en pruebas

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    MAIL_DEBUG = False  # Desactiva depuración de correos
    SESSION_COOKIE_SECURE = True  # Cookies seguras en producción
