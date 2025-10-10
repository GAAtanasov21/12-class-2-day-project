from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.order_service import create_order, list_orders
from services.cart_service import get_cart, clear_cart
from fpdf import FPDF
from flask import send_file
order_bp = Blueprint("order", __name__, url_prefix="/order")


import tempfile
from flask import send_file

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

            # Generate PDF invoice
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Order Confirmation - Order #{order.id}", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Customer ID: {user_id}", ln=True)
            pdf.cell(200, 10, txt=f"Shipping Address: {address}", ln=True)
            pdf.cell(200, 10, txt=f"Payment Method: {payment}", ln=True)
            pdf.cell(200, 10, txt=f"Total: ${order.total:.2f}", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Items:", ln=True)

            for item in cart:
                product = item["product"]
                quantity = item["quantity"]
                size = item["size"]
                line = f"{product.name} (Size {size}) x {quantity} - ${product.price * quantity:.2f}"
                pdf.cell(200, 10, txt=line, ln=True)

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(temp_file.name)

            clear_cart(user_id)
            flash(f"Order #{order.id} placed successfully!")

            return send_file(temp_file.name, as_attachment=True)

        except ValueError as e:
            flash(str(e))
            return redirect(url_for("order.checkout"))

    return render_template("checkout.html", cart=cart)
