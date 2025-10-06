from services.models import db, CartItem, Product


def get_cart(user_id):
    """Get all cart items for a user"""
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    # Format to match old structure for templates
    formatted_cart = []
    for item in cart_items:
        formatted_cart.append({
            "product": item.product,
            "size": item.size,
            "quantity": item.quantity,
            "cart_item_id": item.id
        })

    return formatted_cart


def add_to_cart(user_id, product_id, size=None, quantity=1):
    """Add product to cart"""
    product = Product.query.get(product_id)

    if not product:
        return False, "Product not found"

    if product.stock < quantity:
        return False, "Not enough stock"

    if not size:
        return False, "Size is required"

    # Check if item already exists in cart
    existing_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        size=int(size)
    ).first()

    if existing_item:
        # Update quantity
        existing_item.quantity += quantity
        db.session.commit()
        return True, "Cart updated"
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            size=int(size),
            quantity=quantity
        )
        db.session.add(cart_item)
        db.session.commit()
        return True, "Added to cart"


def remove_from_cart(user_id, product_id):
    """Remove product from cart"""
    cart_items = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).all()

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    return True


def clear_cart(user_id):
    """Clear all items from user's cart"""
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return True


def get_cart_count(user_id):
    """Get total number of items in cart"""
    return CartItem.query.filter_by(user_id=user_id).count()