from flask import Blueprint, render_template

signin_bp = Blueprint('signin', __name__, url_prefix='/showSignIn')

@signin_bp.route('/')
def signin():
    return render_template('signin.html')