import os
import textwrap
from datetime import datetime, timedelta
from functools import wraps
import requests
import jwt
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from marshmallow import Schema, ValidationError, fields, validate
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from app.views import Response, get_response

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, error="ユーザー名が空でないため登録・ログインできません。"))
    email = fields.Email()
    password = fields.Str(required=True, validate=validate.Length(min=6, error=f"パスワードは６文字以上でなければなりません。"))
    id = fields.Int()
    create_at = fields.DateTime()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return jsonify({"message": "Authentication Token is missing!",
                            "data": None,
                            "error": "Unauthorized"}), 401

        try:
            key = os.getenv("SECRET_KEY")
            data = jwt.decode(token, key, algorithms=['HS256'])
            user_id = data["user_id"]
            db = get_db()
            cur = db.cursor(dictionary=True)
            g.user = (
                cur.execute(f"select * from users where id = {user_id}").fetchone()
            )
            if g.user is None:
                return jsonify({
                           "message": "Invalid Authentication token!",
                           "data": None,
                           "error": "Unauthorized"
                       }), 401

        except Exception as error:
            return jsonify({'message': 'Token is invalid !!',
                            "data": None,
                            "error": str(error)}), 500

        return f(token, *args, **kwargs)

    return decorated


def signin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.signin"))

        return view(**kwargs)

    return wrapped_view


@auth_bp.route('/signin', methods=('GET', 'POST'))
def signin():
    response = Response()
    schema = UserSchema()

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor(dictionary=True)
        error = None

        if db.is_connected():
            print("Connected")
        else:
            print("Not connected")

        response.data = {
            "username": username,
            "password": password
        }

        try:
            result = schema.load(response.data)
        except ValidationError as err:
            error = err.messages
            response.status = "fail"
            response.message = f"サインイン失敗。{error}"

        if error is None:
            query = textwrap.dedent(
                f"""
                select * from users where username = '{username}';
                """
            )
            cur.execute(query)
            user = cur.fetchone()

            if user is None:
                error = "ユーザー名が間違っています。"
                response.status = "fail"
                response.message = f"サインイン失敗。{error}"
            elif not check_password_hash(user["password"], password):
                error = "パスワードが間違っています。"
                response.status = "fail"
                response.message = f"サインイン失敗。{error}"
            else:
                # store the user id in a new session and return to the index
                session.clear()
                session["user_id"] = user["id"]
                response.data["id"] = user["id"]
                response.message = "サインイン成功"
                key = os.getenv("SECRET_KEY")
                token = jwt.encode({
                    "user_id": user["id"],
                    "exp": datetime.utcnow()+ timedelta(minutes=30)
                }, key, algorithm="HS256")
                response.token = token

                url = "http://127.0.0.1:3000/auth/signin"
                header = {"Authorization": token}
                r = requests.post(url, headers=header)

            return get_response(response, 200)

        flash(error)
        return get_response(response, 200)

    return render_template("auth/signin.html")


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    response = Response()
    schema = UserSchema()

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        cur = db.cursor(dictionary=True)
        error = None

        if db.is_connected():
            print("Connected")
        else:
            print("Not connected")

        response.data = {
            "username": username,
            "password": password,
            "email": email
        }

        try:
            result = schema.load(response.data)
        except ValidationError as err:
            error = err.messages
            response.status = "fail"
            response.message = f"登録失敗。{error}"

        if error is None:
            try:
                query = textwrap.dedent(
                    f"""
                    insert into users (username, email, password)values ('{username}','{email}','{generate_password_hash(password)}'); 
                    """
                )
                cur.execute(query)
                db.commit()
                response.message = "登録成功"
            except db.InterityError:
                response.status = "fail"
                error = f"User {username} is already registered."
                response.message = f"登録失敗。{error}"

            return get_response(response, 200)

        flash(error)
        return get_response(response, 200)

    return render_template("auth/signup.html")


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))
