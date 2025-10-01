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


def list_products(query=None, color=None, min_price=None, max_price=None, size=None, in_stock=False, category=None, sort_by=None):
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

    if sort_by:
        results = sort_products(results, sort_by)

    return results


def sort_products(products_list, sort_by):
    if not products_list or len(products_list) <= 1:
        return products_list

    if sort_by == 'name_asc':
        return quick_sort(products_list, key=lambda p: p.name.lower(), reverse=False)
    elif sort_by == 'name_desc':
        return quick_sort(products_list, key=lambda p: p.name.lower(), reverse=True)
    elif sort_by == 'price_asc':
        return quick_sort(products_list, key=lambda p: p.price, reverse=False)
    elif sort_by == 'price_desc':
        return quick_sort(products_list, key=lambda p: p.price, reverse=True)

    return products_list


def quick_sort(arr, key=None, reverse=False):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    pivot_value = key(pivot) if key else pivot

    left = []
    middle = []
    right = []

    for item in arr:
        item_value = key(item) if key else item
        if item_value < pivot_value:
            left.append(item)
        elif item_value > pivot_value:
            right.append(item)
        else:
            middle.append(item)

    if reverse:
        return quick_sort(right, key, reverse) + middle + quick_sort(left, key, reverse)
    else:
        return quick_sort(left, key, reverse) + middle + quick_sort(right, key, reverse)


def get_product(pid):

    for p in products:
        if p.id == pid:
            return p
    return None


def get_product_category(product):
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
    add_product("Speed Racer", "Professional racing shoes", "Red", [39, 40, 41, 42], 129.99, 8, "running")
    add_product("Oxford Classic", "Elegant formal shoes", "Black", [40, 41, 42, 43, 44], 149.99, 12, "official")