from services.models import Product

products = []

def add_product(name, description, color, sizes, price, stock):
    p = Product(name, description, color, sizes, price, stock)
    products.append(p)
    return p

def list_products():
    return products.copy()

def get_product(pid):
    return next((p for p in products if p.id == pid), None)

def init_sample_products():
    if products:
        return
    add_product("AirMax Runner", "Lightweight running shoes", "Black", [40,41,42,43], 89.99, 10)
    add_product("Classic Sneakers", "Everyday casual sneakers", "White", [38,39,40,41,42], 59.99, 15)
    add_product("Mountain Boots", "Durable boots for hiking", "Brown", [42,43,44,45], 120.00, 5)
