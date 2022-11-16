from flask import Blueprint, render_template

signup_bp = Blueprint('signup', __name__, url_prefix='/showSignUp')

@signup_bp.route('/')
def signup():
    return render_template('signup.html')