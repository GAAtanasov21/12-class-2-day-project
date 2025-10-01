from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from services.cart_service import add_to_cart, get_cart, remove_from_cart

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

def login_required():
    return "user_email" in session

@cart_bp.route("/")
def view_cart():
    if not login_required():
        flash("Login required")
        return redirect(url_for("auth.login"))
    user_email = session["user_email"]
    cart = get_cart(user_email)
    total = sum(item["product"].price * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

@cart_bp.route("/add/<int:product_id>")
def add(product_id):
    if not login_required():
        flash("Login required")
        return redirect(url_for("auth.login"))

    user_email = session["user_email"]
    size = request.args.get("size")
    if not size:
        flash("You must select a size")
        return redirect(url_for("catalog.catalog"))

    success, msg = add_to_cart(user_email, product_id, size)
    flash(msg)
    return redirect(url_for("catalog.catalog"))


@cart_bp.route("/remove/<int:product_id>")
def remove(product_id):
    if not login_required():
        flash("Login required")
        return redirect(url_for("auth.login"))
    user_email = session["user_email"]
    remove_from_cart(user_email, product_id)
    flash("Item removed from cart")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/out_of_stock")
def out_of_stock():
    return render_template("out_of_stock.html")