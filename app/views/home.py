from flask import Blueprint, render_template, request, redirect, url_for, abort


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/admin')
def admin():
    abort(500)