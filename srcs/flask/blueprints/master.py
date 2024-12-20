# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    master.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/12/20 15:27:37 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 15:35:28 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint
from config import BlueprintConfig as config

master_bp = Blueprint('master', __name__)

if config.USERS:
    from .users import users_bp
    master_bp.register_blueprint(users_bp)

if config.LIKES:
    from .likes import likes_bp
    master_bp.register_blueprint(likes_bp)

if config.NOTIFICATIONS:
    from .notifications import notifications_bp
    master_bp.register_blueprint(notifications_bp)

if config.INTERESTS:
    from .interests import interests_bp
    master_bp.register_blueprint(interests_bp)

if config.CHAT:
    from .chat import chat_bp
    master_bp.register_blueprint(chat_bp)

if config.PROFILE:
    from .profile import profile_bp
    master_bp.register_blueprint(profile_bp)

if config.PICTURES:
    from .pictures import pictures_bp
    master_bp.register_blueprint(pictures_bp)

if config.EXAMPLE:
    from .example import example_bp
    master_bp.register_blueprint(example_bp)

if config.CUSTOM_ERRORS:
    from .custom_errors import error_bp
    master_bp.register_blueprint(error_bp)

