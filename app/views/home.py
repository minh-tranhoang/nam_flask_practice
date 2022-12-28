from flask import (
    Blueprint,
    abort,
    jsonify,
    render_template
)

from app.views.auth import token_required

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@token_required
def home(token):
    if token is not None:
        return jsonify(token)
    return render_template('home.html')


@home_bp.route('/admin')
@token_required
def admin():
    abort(500)
