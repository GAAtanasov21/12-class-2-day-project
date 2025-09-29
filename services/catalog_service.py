from services.models import Product, RunningShoe, EverydayShoe, OfficialShoe, MountainShoe

products = []


def add_product(name, description, color, sizes, price, stock, category=None):
    if category == 'running':
        p = RunningShoe(name, description, color, sizes, price, stock)
    elif category == 'everyday':
        p = EverydayShoe(name, description, color, sizes, price, stock)
    elif category == 'official':
        p = OfficialShoe(name, description, color, sizes, price, stock)
    elif category == 'mountain':
        p = MountainShoe(name, description, color, sizes, price, stock)
    else:
        p = Product(name, description, color, sizes, price, stock)

    products.append(p)
    return p


def list_products(query=None, color=None, min_price=None, max_price=None, size=None, in_stock=False, category=None):
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

    if category:
        category_map = {
            'running': RunningShoe,
            'everyday': EverydayShoe,
            'official': OfficialShoe,
            'mountain': MountainShoe
        }
        if category in category_map:
            results = [p for p in results if isinstance(p, category_map[category])]

    return results


def get_product(pid):
    for p in products:
        if p.id == pid:
            return p
    return None


def get_product_category(product):
    """Return the category name of a product"""
    if isinstance(product, RunningShoe):
        return 'running'
    elif isinstance(product, EverydayShoe):
        return 'everyday'
    elif isinstance(product, OfficialShoe):
        return 'official'
    elif isinstance(product, MountainShoe):
        return 'mountain'
    return 'general'


def init_sample_products():
    if products:
        return
    add_product("AirMax Runner", "Lightweight running shoes", "Black", [40, 41, 42, 43], 89.99, 10, "running")
    add_product("Classic Sneakers", "Everyday casual sneakers", "White", [38, 39, 40, 41, 42], 59.99, 15, "everyday")
    add_product("Mountain Boots", "Durable boots for hiking", "Brown", [42, 43, 44, 45], 120.00, 5, "mountain")