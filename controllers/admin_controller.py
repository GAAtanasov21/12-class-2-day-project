from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from services.catalog_service import list_products, add_product, get_product, get_product_category
from services.auth_service import users, get_user
from services.order_service import list_orders

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def check_admin():
    if not session.get("user_email"):
        flash("Login required")
        return redirect(url_for("auth.login"))
    if not session.get("is_admin"):
        flash("Admin access required")
        return redirect(url_for("index"))


@admin_bp.route("/")
def dashboard():
    return render_template("admin_dashboard.html")


@admin_bp.route("/products")
def manage_product():
    sort_by = request.args.get("sort_by")

    products = list_products(sort_by=sort_by)

    products_with_category = []
    for p in products:
        category = get_product_category(p)
        products_with_category.append({
            'product': p,
            'category': category
        })
    return render_template("admin_products.html", products_with_category=products_with_category)


@admin_bp.route("/products/add", methods=["GET", "POST"])
def add_product_route():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        desc = request.form.get("description", "").strip()
        color = request.form.get("color", "").strip()
        sizes = [int(s) for s in request.form.get("sizes", "").split(",") if s.strip().isdigit()]
        price = float(request.form.get("price", 0))
        stock = int(request.form.get("stock", 0))
        category = request.form.get("category", "")

        add_product(name, desc, color, sizes, price, stock, category)
        flash(f"Product {name} added to {category} category")
        return redirect(url_for("admin.manage_product"))
    return render_template("admin_product_form.html", action="Add", product=None, category=None)


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found")
        return redirect(url_for("admin.manage_product"))

    current_category = get_product_category(product)

    if request.method == "POST":
        product.name = request.form.get("name", "").strip()
        product.description = request.form.get("description", "").strip()
        product.color = request.form.get("color", "").strip()
        product.sizes = [int(s) for s in request.form.get("sizes", "").split(",") if s.strip().isdigit()]
        product.price = float(request.form.get("price", product.price))
        product.stock = int(request.form.get("stock", product.stock))
        flash(f"Product {product.name} updated")
        return redirect(url_for("admin.manage_product"))
    return render_template("admin_product_form.html", action="Edit", product=product, category=current_category)


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


@admin_bp.route("/users")
def manage_users():
    all_users = list(users.values())
    return render_template("admin_users.html", users=all_users)


@admin_bp.route("/users/toggle_admin/<email>", methods=["POST"])
def toggle_admin(email):
    user = get_user(email)
    if not user:
        flash("User not found.")
    elif user.email == session.get("user_email"):
        flash("You cannot change your own admin status.")
    else:
        user.is_admin = not user.is_admin
        flash(f"{'Promoted' if user.is_admin else 'Demoted'} {user.email}.")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/users/delete/<email>", methods=["POST"])
def delete_user(email):
    user = get_user(email)
    if not user:
        flash("User not found.")
    elif user.email == session.get("user_email"):
        flash("You cannot delete yourself.")
    else:
        users.pop(user.email, None)
        flash(f"User {user.email} deleted.")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/orders")
def view_orders():
    all_orders = list_orders()
    return render_template("admin_orders.html", orders=all_orders)