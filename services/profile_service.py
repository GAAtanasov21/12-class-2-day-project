import os
import uuid
from werkzeug.utils import secure_filename
from services.models import db, User


def upload_profile_picture(user_id, file):
    """Upload and save profile picture (pending admin approval)"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"

    # Create upload directory if not exists
    upload_folder = 'static/uploads/profiles'
    os.makedirs(upload_folder, exist_ok=True)

    # Delete old picture if exists
    if user.profile_picture:
        old_file = os.path.join(upload_folder, user.profile_picture)
        if os.path.exists(old_file):
            os.remove(old_file)

    # Save new file
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Update user record
    user.profile_picture = filename
    user.profile_picture_status = 'pending'  # Awaiting admin approval
    db.session.commit()

    return True, "Profile picture uploaded! Waiting for admin approval."


def approve_profile_picture(user_id):
    """Admin approves profile picture"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    if user.profile_picture_status != 'pending':
        return False, "No pending profile picture"

    user.profile_picture_status = 'approved'
    db.session.commit()

    return True, f"Profile picture approved for {user.email}"


def reject_profile_picture(user_id, reason=None):
    """Admin rejects profile picture"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    if user.profile_picture_status != 'pending':
        return False, "No pending profile picture"

    # Delete the file
    if user.profile_picture:
        file_path = os.path.join('static/uploads/profiles', user.profile_picture)
        if os.path.exists(file_path):
            os.remove(file_path)

    user.profile_picture = None
    user.profile_picture_status = 'rejected'
    db.session.commit()

    return True, f"Profile picture rejected for {user.email}"


def get_pending_profile_pictures():
    """Get all users with pending profile pictures"""
    return User.query.filter_by(profile_picture_status='pending').all()


def get_profile_picture_stats():
    """Get statistics about profile pictures"""
    total_users = User.query.count()
    approved = User.query.filter_by(profile_picture_status='approved').count()
    pending = User.query.filter_by(profile_picture_status='pending').count()

    return {
        'total_users': total_users,
        'approved': approved,
        'pending': pending,
        'no_picture': total_users - approved - pending
    }