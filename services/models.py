from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, PickleType

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, email, password, is_admin=False):
        self.email = email.lower().strip()
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    color = Column(String(50))
    sizes = Column(PickleType)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    product_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    reviews = db.relationship('ProductReview', backref='product', lazy=True, cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': product_type
    }

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

    def calculate_discount(self, discount_percent):
        return self.price * (1 - discount_percent / 100)

    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)

    def get_rating_count(self):
        """Get total number of ratings"""
        return len(self.reviews)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class RunningShoe(Product):
    __mapper_args__ = {
        'polymorphic_identity': 'running',
    }

    def get_category_display(self):
        return "Running Shoes - Lightweight & Fast"

    def get_product_type(self):
        return "running"

    def get_performance_rating(self):
        return "High Performance"


class EverydayShoe(Product):
    __mapper_args__ = {
        'polymorphic_identity': 'everyday',
    }

    def get_category_display(self):
        return "Everyday Shoes - Casual & Comfortable"

    def get_product_type(self):
        return "everyday"

    def get_comfort_rating(self):
        return "Maximum Comfort"


class OfficialShoe(Product):
    __mapper_args__ = {
        'polymorphic_identity': 'official',
    }

    def get_category_display(self):
        return "Official Shoes - Elegant & Professional"

    def get_product_type(self):
        return "official"

    def get_formality_level(self):
        return "Formal"


class MountainShoe(Product):
    __mapper_args__ = {
        'polymorphic_identity': 'mountain',
    }

    def get_category_display(self):
        return "Mountain Shoes - Durable & Rugged"

    def get_product_type(self):
        return "mountain"

    def get_durability_rating(self):
        return "Extra Durable"


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    address = Column(Text, nullable=False)
    payment_method = Column(String(50), nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def get_order_summary(self):
        return f"Order #{self.id} - ${self.total:.2f} - {len(self.items)} items"

    def __repr__(self):
        return f"<Order {self.id} by User {self.user_id}, total={self.total}>"


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

    def __repr__(self):
        return f"<OrderItem {self.product_name} x{self.quantity}>"


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    size = Column(Integer, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

    def __repr__(self):
        return f"<CartItem User:{self.user_id} Product:{self.product_id}>"


class ProductReview(db.Model):
    """Product reviews with rating and comment"""
    __tablename__ = 'product_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='reviews')

    def __repr__(self):
        return f"<ProductReview Product:{self.product_id} by User:{self.user_id} Rating:{self.rating}>"


class Comments(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='comments')

    def __repr__(self):
        return f"<Comments User:{self.user_id}>"