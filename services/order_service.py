from services.models import db, Order, OrderItem, Product


def create_order(user_id, cart_items, address, payment_method):
    """
    Create order from cart items
    cart_items format: [{"product": Product, "size": int, "quantity": int}, ...]
    """
    order_items = []
    total = 0.0

    # Validate and prepare order items
    for item in cart_items:
        product = item["product"]
        quantity = item["quantity"]
        size = item["size"]

        # Check stock
        if product.stock < quantity:
            raise ValueError(f"Not enough stock for {product.name}")

        # Reduce stock
        product.reduce_stock(quantity)

        # Calculate subtotal
        subtotal = product.price * quantity
        total += subtotal

        # Create order item data
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "size": size,
            "price_at_purchase": product.price,
            "subtotal": subtotal
        })

    # Create order
    order = Order(
        user_id=user_id,
        address=address,
        payment_method=payment_method,
        total=total
    )

    db.session.add(order)
    db.session.flush()  # Get order ID before adding items

    # Create order items
    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product_id"],
            product_name=item_data["product_name"],
            quantity=item_data["quantity"],
            size=item_data["size"],
            price_at_purchase=item_data["price_at_purchase"],
            subtotal=item_data["subtotal"]
        )
        db.session.add(order_item)

    db.session.commit()
    return order


def list_orders():
    """Get all orders"""
    return Order.query.order_by(Order.created_at.desc()).all()


def get_user_orders(user_id):
    """Get orders for specific user"""
    return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()


def get_order(order_id):
    """Get order by ID"""
    return Order.query.get(order_id)