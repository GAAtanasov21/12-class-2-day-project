from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod

class User:
    _next_id = 1

    def __init__(self, email, password, is_admin=False):
        self.__id = User._next_id
        User._next_id += 1
        self.__email = email.lower().strip()
        self.__password_hash = generate_password_hash(password)
        self.__is_admin = is_admin

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        if isinstance(value, bool):
            self.__is_admin = value
        else:
            raise ValueError("is_admin must be a boolean")

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def __repr__(self):
        return f"<User {self.__email}>"


class ProductBase(ABC):

    @abstractmethod
    def get_category_display(self):
        pass

    @abstractmethod
    def get_product_type(self):
        pass

    def calculate_discount(self, discount_percent):
        """Concrete method available to all products"""
        return self.price * (1 - discount_percent / 100)

class Product(ProductBase):
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

    def is_available(self):
        return self.stock > 0

    def get_category_display(self):
        return "General Product"

    def get_product_type(self):
        return "general"

    def __str__(self):
        return f"{self.name} - ${self.price}"


class RunningShoe(Product):
    """
    Polymorphism: Overrides parent methods with specific implementation
    """

    def __init__(self, name, description, color, sizes, price, stock):
        super().__init__(name, description, color, sizes, price, stock)
        self.shoe_type = "Running"

    def get_category_display(self):
        return "Running Shoes - Lightweight & Fast"

    def get_product_type(self):
        return "running"

    def get_performance_rating(self):
        return "High Performance"


class EverydayShoe(Product):

    def __init__(self, name, description, color, sizes, price, stock):
        super().__init__(name, description, color, sizes, price, stock)
        self.shoe_type = "Everyday"

    def get_category_display(self):
        return "Everyday Shoes - Casual & Comfortable"

    def get_product_type(self):
        return "everyday"

    def get_comfort_rating(self):
        return "Maximum Comfort"


class OfficialShoe(Product):

    def __init__(self, name, description, color, sizes, price, stock):
        super().__init__(name, description, color, sizes, price, stock)
        self.shoe_type = "Official"

    def get_category_display(self):
        return "Official Shoes - Elegant & Professional"

    def get_product_type(self):
        return "official"

    def get_formality_level(self):
        return "Formal"


class MountainShoe(Product):

    def __init__(self, name, description, color, sizes, price, stock):
        super().__init__(name, description, color, sizes, price, stock)
        self.shoe_type = "Mountain"

    def get_category_display(self):
        return "Mountain Shoes - Durable & Rugged"

    def get_product_type(self):
        return "mountain"

    def get_durability_rating(self):
        return "Extra Durable"


class Order:
    _next_id = 1

    def __init__(self, user_email, items, address, payment_method):
        self.__id = Order._next_id
        Order._next_id += 1
        self.__user_email = user_email
        self.__items = items
        self.__address = address
        self.__payment_method = payment_method
        self.__created_at = datetime.now()
        self.__total = sum(item["subtotal"] for item in items)

    # Getters (Properties)
    @property
    def id(self):
        return self.__id

    @property
    def user_email(self):
        return self.__user_email

    @property
    def items(self):
        return self.__items.copy()  # Return copy to prevent external modification

    @property
    def address(self):
        return self.__address

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def created_at(self):
        return self.__created_at

    @property
    def total(self):
        return self.__total

    def get_order_summary(self):
        return f"Order #{self.__id} - ${self.__total:.2f} - {len(self.__items)} items"

    def __repr__(self):
        return f"<Order {self.__id} by {self.__user_email}, total={self.__total}>"