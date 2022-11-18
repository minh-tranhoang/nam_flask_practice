from flask import Blueprint, request, session
from flask import flash, render_template, redirect, url_for
from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import textwrap

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn, cur = get_db(dict_cursor=True)
        error = None

        query = textwrap.dedent(
            f"""
            select * from users where username = '{username}';
            """
        )
        print(query)
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
            return redirect(url_for("index"))
        
        flash(error)

    return render_template("auth/signin.html")

@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        conn, cur = get_db()
        error = None

        if (conn.is_connected()):
            print("Connected")
        else:
            print("Not connected")

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                print("OK-1")
                query = textwrap.dedent(
                    f"""
                    insert into users (username, email, password)values ('{username}','{email}','{generate_password_hash(password)}');
                    """
                )
                cur.execute(query)
                conn.commit()
            except:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.signin"))

        flash(error)

    return render_template("auth/signup.html")