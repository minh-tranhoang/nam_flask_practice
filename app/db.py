import os
import textwrap
import click
import mysql.connector as db
from dotenv import load_dotenv
from flask import current_app, g

load_dotenv()
username = os.getenv('DB_USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
db_name = os.getenv('DATABASE')


def get_db():
    if "db" not in g:
        try:
            g.db = db.connect(
                host=host,
                db=db_name,
                user=username,
                password=password
            )

            return g.db
        except db.Error as e:
            print("###\t ", e)
            return None


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
      db.close()


def init_db():
    db = get_db()
    with open('db/db.sql', 'r') as f:
        create_table_query = textwrap.dedent(f.read())
        with db.cursor() as cur:
            cur.excute(create_table_query, multi=True)
        db.commit()


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
