from flask import Blueprint, request, session
from flask import flash, render_template, redirect, url_for
from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import textwrap
from app.views import Response, get_response
from marshmallow import Schema, ValidationError, validate, fields


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, error="ユーザー名が空でないため登録・ログインできません。"))
    email = fields.Email()
    password = fields.Str(required=True, validate=validate.Length(min=6, error=f"パスワードは６文字以上でなければなりません。"))
    id = fields.Int()
    create_at = fields.DateTime()


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

        query = textwrap.dedent(
            f"""
            select * from users where username = '{username}';
            """
        )
        cur.execute(query)
        user = cur.fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            response.result = {
                "id": user["id"],
                "username": username,
                "password": password
            }
            response.message = "ログイン成功"

            return get_response(response, 200)

        response.result = {
            "username": username,
            "password": password
        }
        response.message = f"ログイン失敗。エラー：　{error}"
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

        response.result = {
            "username": username,
            "password": password,
            "email": email
        }

        try:
            result = schema.load(response.result)
        except ValidationError as err:
            error = err.messages
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
                error = f"User {username} is already registered."
                response.message = f"登録失敗。{error}"

            return get_response(response, 200)

        flash(error)
        return get_response(response, 200)

    return render_template("auth/signup.html")
