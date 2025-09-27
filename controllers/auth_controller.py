from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import render_template, redirect, url_for, flash
from services.auth_service import create_user, get_user, verify_user, init_sample_data

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods = ["GET", "POST"])
def login():
    init_sample_data()
    if request.method == "POST":
        email = (request.form.get("email") or "").lower().strip()
        password = request.form.get("password") or ""
        if verify_user(email, password):
            user = get_user(email)
            session["user_email"] = user.email
            session["is_admin"] = user.is_admin
            flash(f"Logged in as {user.email}")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))
    return render_template("login.html")

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = (request.form.get("email") or "").lower().strip()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("auth.register"))
        if get_user(email):
            flash("A user with that email already exists.")
            return redirect(url_for("auth.register"))
        create_user(email, password)
        print(f"[SIMULATED EMAIL] Confirmation sent to {email}")
        flash("Registration successful. Check server console for confirmation message.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_email", None)
    session.pop("is_admin", None)
    flash("Logged out.")
    return redirect(url_for("index"))