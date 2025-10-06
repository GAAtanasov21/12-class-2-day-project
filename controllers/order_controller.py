from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.order_service import create_order, list_orders
from services.cart_service import get_cart, clear_cart

order_bp = Blueprint("order", __name__, url_prefix="/order")


@order_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get("user_id"):
        flash("You must be logged in to place an order.")
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")
    cart = get_cart(user_id)

    if not cart:
        flash("Your cart is empty.")
        return redirect(url_for("catalog.catalog"))

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        payment = request.form.get("payment", "").strip()

        if not address or not payment:
            flash("Address and payment method are required.")
            return redirect(url_for("order.checkout"))

        try:
            order = create_order(user_id, cart, address, payment)
            clear_cart(user_id)
            flash(f"Order #{order.id} placed successfully!")
            return redirect(url_for("index"))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("order.checkout"))

    return render_template("checkout.html", cart=cart)