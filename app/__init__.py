import os
from flask import Flask, render_template, url_for, jsonify
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from dotenv import load_dotenv

load_dotenv()


def create_app(config_name):
    app = Flask(__name__)
    env = os.getenv('ENV')

    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(TestingConfig)

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    register_blueprints(app)
    register_error_handlers(app)

    app.add_url_rule("/", endpoint="index")

    return app


def register_blueprints(app):
    from app.views.home import home_bp
    from app.views.auth import auth_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": True, "message": "Bad Request - The page isn't working at the moment"}), e.code

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": True, "message": "Forbidden - You don't have permission to access on this server."}), e.code

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": True, "message": "Not Found - The specified file was not found on this website. "
                                                  "Please check the URL for mistakes and try again."}), e.code

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": True, "message": "Method not allowed - This browser is not supported."}), e.code

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": True, "message": "Internal Server Error - This browser is not supported."}), e.code
