from flask import Flask, render_template, url_for

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    register_blueprints(app)
    register_error_handlers(app)

    return app

def register_blueprints(app):
    from app.views.home import home_bp
    from app.views.signin import signin_bp
    from app.views.signup import signup_bp 
    
    app.register_blueprint(home_bp)
    app.register_blueprint(signin_bp)
    app.register_blueprint(signup_bp)


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
