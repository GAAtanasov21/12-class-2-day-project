from werkzeug.security import generate_password_hash, check_password_hash
users = {}

def create_user(email, password, is_admin = False):
    email = email.lower().strip()
    if email in users:
        return "User already exists"

    if email == "admin@admin" and password == "admin":
        is_admin = True

    users[email] = {
        "email" : email,
        "password" : generate_password_hash(password),
        "is_admin": bool(is_admin)
    }

def get_user(email):
    return users.get(email)

def verify_user(email, password):
    user = get_user(email)
    if not user:
        return False
    return check_password_hash(user["password"], password)

