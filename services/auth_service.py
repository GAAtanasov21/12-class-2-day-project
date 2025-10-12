from services.models import db, User


def create_user(email, password, is_admin=False):
    """Create a new user"""
    existing_user = User.query.filter_by(email=email.lower()).first()
    if existing_user:
        return None

    user = User(email=email, password=password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user


def get_user(email):
    """Get user by email"""
    return User.query.filter_by(email=email.lower()).first()


def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)


def verify_user(email, password):
    """Verify user credentials"""
    user = get_user(email)
    return user and user.check_password(password)


def get_all_users():
    """Get all users"""
    return User.query.all()


def delete_user(email):
    """Delete user by email"""
    user = get_user(email)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


def toggle_admin_status(email):
    """Toggle admin status for a user"""
    user = get_user(email)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
        return True
    return False


def change_password(user_id, new_password):
    """Change user password"""
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found"

    user.set_password(new_password)
    db.session.commit()
    return True, "Password changed successfully"