from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

class User:
    _next_id = 1
    def __init__(self, email, password, is_admin=False):
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
        self.sizes = sizes
        self.price = float(price)
        self.stock = int(stock)
    def reduce_stock(self, amount):
        if amount > self.stock:
            return False
        self.stock -= amount
        return True

class RunningShoe(Product):
    def __init__(self, name, description, color, sizes, price, stock):
        Product.__init__(self, name, description, color, sizes, price, stock)

class EverydayShoe(Product):
    def __init__(self, name, description, color, sizes, price, stock):
        Product.__init__(self, name, description, color, sizes, price, stock)

class OficialShoe(Product):
    def __init__(self, name, description, color, sizes, price, stock):
        Product.__init__(self, name, description, color, sizes, price, stock)

class MountainShoe(Product):
    def __init__(self, name, description, color, sizes, price, stock):
        Product.__init__(self, name, description, color, sizes, price, stock)



class Order:
    _next_id = 1

    def __init__(self, user_email, items, address, payment_method):
        self.id = Order._next_id
        Order._next_id += 1
        self.user_email = user_email
        self.items = items
        self.address = address
        self.payment_method = payment_method
        self.created_at = datetime.now()
        self.total = sum(item["subtotal"] for item in items)

    def __repr__(self):
        return f"<Order {self.id} by {self.user_email}, total={self.total}>"

