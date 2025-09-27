from services.catalog_service import get_product

# Store carts per user_email
carts = {}

# Store orders per user_email
orders = {}

def get_cart(user_email):
    return carts.setdefault(user_email, [])

def add_to_cart(user_email, product_id, quantity=1):
    product = get_product(product_id)
    if not product:
        return False, "Product not found"
    if product.stock < quantity:
        return False, "Not enough stock"
    cart = get_cart(user_email)
    # Check if product already in cart
    for item in cart:
        if item["product"].id == product_id:
            item["quantity"] += quantity
            return True, "Added to cart"
    cart.append({"product": product, "quantity": quantity})
    return True, "Added to cart"

def remove_from_cart(user_email, product_id):
    cart = get_cart(user_email)
    carts[user_email] = [item for item in cart if item["product"].id != product_id]

def clear_cart(user_email):
    carts[user_email] = []

def checkout(user_email, address, payment_method):
    cart = get_cart(user_email)
    if not cart:
        return False, "Cart is empty"
    # Reduce stock
    for item in cart:
        if item["product"].stock < item["quantity"]:
            return False, f"Not enough stock for {item['product'].name}"
    for item in cart:
        item["product"].reduce_stock(item["quantity"])
    # Save order
    order_list = orders.setdefault(user_email, [])
    order_list.append({
        "items": [{"name": i["product"].name, "quantity": i["quantity"], "price": i["product"].price} for i in cart],
        "address": address,
        "payment_method": payment_method
    })
    # Clear cart
    clear_cart(user_email)
    return True, "Order placed successfully"

def get_orders(user_email):
    return orders.get(user_email, [])
