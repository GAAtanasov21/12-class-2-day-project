from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.order_service import create_order, list_orders
from services.cart_service import get_cart, clear_cart

order_bp = Blueprint("order", __name__, url_prefix="/order")

@order_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get("user_email"):
        flash("You must be logged in to place an order.")
        return redirect(url_for("auth.login"))

    cart = get_cart(session.get("user_email"))
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
            order = create_order(session["user_email"], cart, address, payment)
            clear_cart(session["user_email"])
            flash(f"Order #{order.id} placed successfully!")

            return redirect(url_for("index"))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("order.checkout"))

    return render_template("checkout.html", cart=cart)
