import os
import sqlite3
from datetime import timedelta

from flask import Flask, request, session, redirect, render_template
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Use an environment variable in real deployments.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-this-secret"
)

# Secure session configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # True when using HTTPS
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

ph = PasswordHasher()

DATABASE = "users.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()


def validate_username(username):
    if not username:
        return False

    if len(username) < 3 or len(username) > 30:
        return False

    return username.isalnum()


def validate_password(password):
    if not password:
        return False

    return 12 <= len(password) <= 128


@app.route("/", methods=["GET"])
def home():
    if "user_id" in session:
        return f"Logged in as {session['username']}"

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Server-side validation
    if not validate_username(username) or not validate_password(password):
        return "Invalid username or password", 401

    db = get_db()

    user = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    db.close()

    # Generic authentication error
    if user is None:
        return "Invalid username or password", 401

    try:
        ph.verify(user["password_hash"], password)
    except VerifyMismatchError:
        return "Invalid username or password", 401

    # Regenerate session data after authentication
    session.clear()
    session.permanent = True
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return redirect("/")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not validate_username(username):
        return "Invalid username", 400

    if not validate_password(password):
        return "Invalid password", 400

    password_hash = ph.hash(password)

    db = get_db()

    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.close()
        return "Unable to create account", 400

    db.close()

    return "Account created successfully", 201


if __name__ == "__main__":
    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
