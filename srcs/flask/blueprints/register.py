import logging
from flask import Blueprint
from config import BlueprintConfig as config

logger = logging.getLogger(__name__)

def register_to(master_bp):

    if config.USERS:
        try:
            from .users import users_bp
            master_bp.register_blueprint(users_bp)
            logger.info("Registered users blueprint.")
        except Exception as e:
            logger.error(f"Error registering users blueprint: {e}")

    if config.LIKES:
        try:
            from .likes import likes_bp
            master_bp.register_blueprint(likes_bp)
            logger.info("Registered likes blueprint.")
        except Exception as e:
            logger.error(f"Error registering likes blueprint: {e}")

    if config.NOTIFICATIONS:
        try:
            from .notifications import notifications_bp
            master_bp.register_blueprint(notifications_bp)
            logger.info("Registered notifications blueprint.")
        except Exception as e:
            logger.error(f"Error registering notifications blueprint: {e}")

    if config.INTERESTS:
        try:
            from .interests import interests_bp
            master_bp.register_blueprint(interests_bp)
            logger.info("Registered interests blueprint.")
        except Exception as e:
            logger.error(f"Error registering interests blueprint: {e}")

    if config.CHAT:
        try:
            from .chat import chat_bp
            master_bp.register_blueprint(chat_bp)
            logger.info("Registered chat blueprint.")
        except Exception as e:
            logger.error(f"Error registering chat blueprint: {e}")

    if config.PROFILE:
        try:
            from .profile import profile_bp
            master_bp.register_blueprint(profile_bp)
            logger.info("Registered profile blueprint.")
        except Exception as e:
            logger.error(f"Error registering profile blueprint: {e}")

    if config.PICTURES:
        try:
            from .pictures import pictures_bp
            master_bp.register_blueprint(pictures_bp)
            logger.info("Registered pictures blueprint.")
        except Exception as e:
            logger.error(f"Error registering pictures blueprint: {e}")

    if config.EXAMPLE:
        try:
            from .example import example_bp
            master_bp.register_blueprint(example_bp)
            logger.info("Registered example blueprint.")
        except Exception as e:
            logger.error(f"Error registering example blueprint: {e}")

    if config.CUSTOM_ERRORS:
        try:
            from .custom_errors import error_bp
            master_bp.register_blueprint(error_bp)
            logger.info("Registered custom errors blueprint.")
        except Exception as e:
            logger.error(f"Error registering custom errors blueprint: {e}")

    if config.USER_TESTING:
        try:
            from testing.user_testing1 import test_user_bp
            master_bp.register_blueprint(test_user_bp)
            logger.info("Registered user testing blueprint.")
        except Exception as e:
            logger.error(f"Error registering user testing blueprint: {e}")

    if config.COOKIE_TESTING:
        try:
            from testing.cookie_testing import test_cookie_bp
            master_bp.register_blueprint(test_cookie_bp)
            logger.info("Registered cookie testing blueprint.")
        except Exception as e:
            logger.error(f"Error registering cookie testing blueprint: {e}")

    if config.DEBUG:
        try:
            from testing.debug import debug_bp
            master_bp.register_blueprint(debug_bp)
            logger.info("Registered debug blueprint.")
            from flask import redirect, url_for
            @master_bp.route('/')
            def redirect_to_list_routes():
                return redirect(url_for('debug.serve_list_routes'))
        except Exception as e:
            logger.error(f"Error registering debug blueprint: {e}")