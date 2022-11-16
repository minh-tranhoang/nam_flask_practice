from flask import Flask, render_template, url_for
from app.views.signup import signup_bp
from app.views.signin import signin_bp
import os

app = Flask(__name__)
app.register_blueprint(signup_bp)
app.register_blueprint(signin_bp)

@app.route("/")
def home():
    return render_template('home.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')