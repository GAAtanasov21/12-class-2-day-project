from services.models import User

users = {}

def create_user(email, password, is_admin=False):
    if email.lower() in users:
        return None
    user = User(email, password, is_admin)
    users[email.lower()] = user
    return user

def get_user(email):
    return users.get(email.lower())

def verify_user(email, password):
    user = get_user(email)
    return user and user.check_password(password)

def init_sample_users():
    if "admin@example.com" not in users:
        create_user("admin@example.com", "admin123", True)
    if "user1@example.com" not in users:
        create_user("user1@example.com", "user123")
    if "user2@example.com" not in users:
        create_user("user2@example.com", "user123")
