from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import create_user, verify_user, get_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").lower().strip()
        password = request.form.get("password") or ""
        if verify_user(email, password):
            user = get_user(email)
            session["user_id"] = user.id  # Store user ID instead of email
            session["user_email"] = user.email
            session["is_admin"] = user.is_admin
            flash(f"Logged in as {user.email}")
            return redirect(url_for("index"))
        flash("Invalid credentials")
        return redirect(url_for("auth.login"))
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = (request.form.get("email") or "").lower().strip()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Email and password required")
            return redirect(url_for("auth.register"))
        if get_user(email):
            flash("Email already exists")
            return redirect(url_for("auth.register"))
        user = create_user(email, password)
        if user:
            print(f"[SIMULATED EMAIL] Confirmation sent to {email}")
            flash("Registration successful. Log in now.")
            return redirect(url_for("auth.login"))
        else:
            flash("Registration failed")
            return redirect(url_for("auth.register"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("index"))