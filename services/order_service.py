from services.models import Order

orders=[]
def create_order(user_email, cart_items, address, payment_method):

    items = []
    for item in cart_items:
        product = item["product"]
        qty = item["quantity"]

        if product.stock < qty:
            raise ValueError(f"Not enough stock for {product.name}")
        product.reduce_stock(qty)

        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": product.price * qty
        })

    order = Order(user_email, items, address, payment_method)
    orders.append(order)
    return order

def list_orders():
    return orders.copy()