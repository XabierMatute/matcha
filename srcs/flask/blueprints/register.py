from flask import Blueprint
from config import BlueprintConfig as config

def register_to(master_bp):

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

    if config.USER_TESTING:
        from testing.user_testing1 import test_user_bp
        master_bp.register_blueprint(test_user_bp)

    if config.COOKIE_TESTING:
        from testing.cookie_testing import test_cookie_bp
        master_bp.register_blueprint(test_cookie_bp)

