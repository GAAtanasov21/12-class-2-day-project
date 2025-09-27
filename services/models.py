from werkzeug.security import generate_password_hash, check_password_hash

class User:
    _next_id = 1

    def __init__(self, email, password, is_admin = False):
        self.id = User._next_id
        User._next_id += 1
        self.email = email.lower().strip()
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product:
    _next_id = 1

    def __init__(self, name, description, color, sizes, price, stock):
        self.id = Product._next_id
        Product._next_id += 1
        self.name = name
        self.description = description
        self.color = color
        self.sizes = sizes  # list of ints
        self.price = float(price)
        self.stock = int(stock)

    def reduce_stock(self, amount):
        if amount > self.stock:
            return "Not enough stock"
        self.stock -= amount