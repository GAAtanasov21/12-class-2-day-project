from services.catalog_service import get_product

# Store carts per user_email
carts = {}

# Store orders per user_email

def get_cart(user_email):
    return carts.setdefault(user_email, [])

def add_to_cart(user_email, product_id, size=None, quantity=1):
    product = get_product(product_id)
    if not product:
        return False, "Product not found"
    if product.stock < quantity:
        return False, "Not enough stock"
    cart = get_cart(user_email)
    for item in cart:
        if item["product"].id == product_id and item.get("size") == size:
            item["quantity"] += quantity
            return True, "Added to cart"
    cart.append({"product": product, "size": size, "quantity": quantity})
    return True, "Added to cart"


def remove_from_cart(user_email, product_id):
    cart = get_cart(user_email)
    carts[user_email] = [item for item in cart if item["product"].id != product_id]

def clear_cart(user_email):
    carts[user_email] = []

