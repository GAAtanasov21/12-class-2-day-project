from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from services.catalog_service import list_products, add_product, get_product, init_sample_products
from services.models import Product
admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
def check_admin():
    if not session.get("user_email"):
        flash("You must be logged in to access the admin panel.")
        return redirect(url_for("auth.login"))
    if not session.get("is_admin"):
        flash("Admin access required.")
        return redirect(url_for("index"))

@admin_bp.route("/")
def dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/products")
def manage_product():
    products = list_products()
    return render_template("admin_products.html", products=products)

@admin_bp.route("/products/add", methods = ['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        color = request.form.get("color", "").strip()
        sizes = request.form.get("sizes", "").split(",")  # e.g., "38,39,40"
        sizes = [int(s.strip()) for s in sizes if s.strip().isdigit()]
        price = float(request.form.get("price", 0))
        stock = int(request.form.get("stock", 0))
        add_product(name, description, color, sizes, price, stock)
        flash(f"Product '{name}' added.")
        return redirect(url_for("admin.manage_product"))
    return render_template("admin_product_form.html", action="Add", product=None)

@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for("admin.manage_product"))

    if request.method == "POST":
        product.name = request.form.get("name", "").strip()
        product.description = request.form.get("description", "").strip()
        product.color = request.form.get("color", "").strip()
        sizes = request.form.get("sizes", "").split(",")
        product.sizes = [int(s.strip()) for s in sizes if s.strip().isdigit()]
        product.price = float(request.form.get("price", product.price))
        product.stock = int(request.form.get("stock", product.stock))
        flash(f"Product '{product.name}' updated.")
        return redirect(url_for("admin.manage_product"))

    return render_template("admin_product_form.html", action="Edit", product=product)

@admin_bp.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = get_product(product_id)
    if product:
        from services.catalog_service import products
        products.remove(product)
        flash(f"Product '{product.name}' deleted.")
    else:
        flash("Product not found.")
    return redirect(url_for("admin.manage_product"))