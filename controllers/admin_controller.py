from flask import Blueprint, render_template, session, redirect, url_for, flash

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def check_admin():
    if not session.get("user_email"):
        flash("You must be logged in to access the admin panel.")
        return redirect(url_for("auth.login"))
    if not session.get("is_admin"):
        flash("Admin access required.")
        return redirect(url_for("index"))

@admin_bp.route("/")
def dashboard():
    return render_template("admin_dashboard.html")