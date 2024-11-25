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

# config/config.py
import os

class Config:
    """Configuración base común para todos los entornos"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    """Configuración específica para el entorno de desarrollo"""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/dev_db')

class TestingConfig(Config):
    """Configuración específica para el entorno de pruebas"""
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/test_db')

class ProductionConfig(Config):
    """Configuración específica para el entorno de producción"""
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/prod_db')


