import os
from flask import Flask, render_template, url_for
from config import config
from dotenv import load_dotenv

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.from_pyfile("../config.py")
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
        return render_template('error/400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('error/405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500
