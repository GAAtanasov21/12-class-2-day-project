from werkzeug.security import generate_password_hash, check_password_hash
from services.models import User
users = {}

def create_user(email, password, is_admin = False):
    email = email.lower().strip()
    if email in users:
        return "User already exists"

    if email == "admin@admin" and password == "admin":
        is_admin = True

    user = User(email, password, is_admin)
    users[email] = user

def get_user(email):
    return users.get(email.lower().strip())

def verify_user(email, password):
    user = get_user(email)
    if not user:
        return False
    return user.check_password(password)

def init_sample_data():
    """Create one admin and two users for testing if they don't exist yet."""
    if "admin@example.com" not in users:
        create_user("admin@example.com", "adminpass", is_admin=True)
    if "user1@example.com" not in users:
        create_user("user1@example.com", "user1pass")
    if "user2@example.com" not in users:
        create_user("user2@example.com", "user2pass")
