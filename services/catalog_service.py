from services.models import Product

products = []

def add_product(name, description, color, sizes, price, stock):
    p = Product(name, description, color, sizes, price, stock)
    products.append(p)
    return p

def list_products(query=None, color=None, min_price=None, max_price=None, size=None, in_stock=False):
    results = products.copy()

    if query:
        results = [p for p in results if query.lower() in p.name.lower() or query.lower() in p.color.lower()]

    if color:
        results = [p for p in results if color.lower() in p.color.lower()]

    if min_price is not None:
        results = [p for p in results if p.price >= min_price]

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if size is not None:
        results = [p for p in results if size in p.sizes]

    if in_stock:
        results = [p for p in results if p.stock > 0]

    return results

def get_product(pid):
    for p in products:
        if p.id == pid:
            return p
    return None

def init_sample_products():
    if products:
        return
    add_product("AirMax Runner", "Lightweight running shoes", "Black", [40,41,42,43], 89.99, 10)
    add_product("Classic Sneakers", "Everyday casual sneakers", "White", [38,39,40,41,42], 59.99, 15)
    add_product("Mountain Boots", "Durable boots for hiking", "Brown", [42,43,44,45], 120.00, 5)
