import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from services.auth_service import get_user_by_id, change_password
from services.profile_service import upload_profile_picture, get_pending_profile_pictures
from services.models import db

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route("/")
def view_profile():
    """View user profile"""
    if not session.get("user_id"):
        flash("Please login to view profile")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(session.get("user_id"))
    if not user:
        flash("User not found")
        return redirect(url_for("index"))

    return render_template("profile.html", user=user)


@profile_bp.route("/edit", methods=["GET", "POST"])
def edit_profile():
    """Edit user profile"""
    if not session.get("user_id"):
        flash("Please login to edit profile")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(session.get("user_id"))
    if not user:
        flash("User not found")
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form.get("action")

        # Change password
        if action == "change_password":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if not current_password or not new_password or not confirm_password:
                flash("All password fields are required")
                return redirect(url_for("profile.edit_profile"))

            if new_password != confirm_password:
                flash("New passwords do not match")
                return redirect(url_for("profile.edit_profile"))

            if not user.check_password(current_password):
                flash("Current password is incorrect")
                return redirect(url_for("profile.edit_profile"))

            if len(new_password) < 6:
                flash("New password must be at least 6 characters")
                return redirect(url_for("profile.edit_profile"))

            success, message = change_password(user.id, new_password)
            flash(message)
            return redirect(url_for("profile.view_profile"))

        # Upload profile picture
        elif action == "upload_picture":
            if 'profile_picture' not in request.files:
                flash("No file selected")
                return redirect(url_for("profile.edit_profile"))

            file = request.files['profile_picture']

            if file.filename == '':
                flash("No file selected")
                return redirect(url_for("profile.edit_profile"))

            if not allowed_file(file.filename):
                flash("Invalid file type. Allowed: PNG, JPG, JPEG, GIF")
                return redirect(url_for("profile.edit_profile"))

            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_FILE_SIZE:
                flash("File size too large. Maximum 5MB")
                return redirect(url_for("profile.edit_profile"))

            success, message = upload_profile_picture(user.id, file)
            flash(message)
            return redirect(url_for("profile.view_profile"))

    return render_template("edit_profile.html", user=user)


@profile_bp.route("/picture/delete", methods=["POST"])
def delete_profile_picture():
    """Delete profile picture"""
    if not session.get("user_id"):
        flash("Please login")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(session.get("user_id"))
    if not user:
        flash("User not found")
        return redirect(url_for("index"))

    if user.profile_picture:
        # Delete file
        file_path = os.path.join('static/uploads/profiles', user.profile_picture)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Update database
        user.profile_picture = None
        user.profile_picture_status = 'none'
        db.session.commit()
        flash("Profile picture deleted")

    return redirect(url_for("profile.view_profile"))