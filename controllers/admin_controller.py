from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from services.catalog_service import list_products, add_product, get_product, get_product_category, delete_product, \
    update_product
from services.auth_service import get_all_users, get_user, delete_user, toggle_admin_status
from services.order_service import list_orders
from services.profile_service import get_pending_profile_pictures, approve_profile_picture, reject_profile_picture

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def check_admin():
    if not session.get("user_id"):
        flash("Login required")
        return redirect(url_for("auth.login"))
    if not session.get("is_admin"):
        flash("Admin access required")
        return redirect(url_for("index"))


@admin_bp.route("/")
def dashboard():
    # Get pending profile pictures count
    pending_pictures = get_pending_profile_pictures()
    return render_template("admin_dashboard.html", pending_count=len(pending_pictures))


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
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        color = request.form.get("color", "").strip()
        sizes = [int(s) for s in request.form.get("sizes", "").split(",") if s.strip().isdigit()]
        price = float(request.form.get("price", product.price))
        stock = int(request.form.get("stock", product.stock))

        update_product(product_id, name, description, color, sizes, price, stock)
        flash(f"Product {name} updated")
        return redirect(url_for("admin.manage_product"))

    return render_template("admin_product_form.html", action="Edit", product=product, category=current_category)


@admin_bp.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product_route(product_id):
    product = get_product(product_id)
    if product:
        product_name = product.name
        delete_product(product_id)
        flash(f"Product '{product_name}' deleted.")
    else:
        flash("Product not found.")
    return redirect(url_for("admin.manage_product"))


@admin_bp.route("/users")
def manage_users():
    all_users = get_all_users()
    return render_template("admin_users.html", users=all_users)


@admin_bp.route("/users/toggle_admin/<email>", methods=["POST"])
def toggle_admin(email):
    user = get_user(email)
    if not user:
        flash("User not found.")
    elif user.email == session.get("user_email"):
        flash("You cannot change your own admin status.")
    else:
        toggle_admin_status(email)
        user = get_user(email)
        flash(f"{'Promoted' if user.is_admin else 'Demoted'} {user.email}.")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/users/delete/<email>", methods=["POST"])
def delete_user_route(email):
    user = get_user(email)
    if not user:
        flash("User not found.")
    elif user.email == session.get("user_email"):
        flash("You cannot delete yourself.")
    else:
        delete_user(email)
        flash(f"User {email} deleted.")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/orders")
def view_orders():
    all_orders = list_orders()
    return render_template("admin_orders.html", orders=all_orders)


@admin_bp.route("/profile-pictures")
def manage_profile_pictures():
    """View all pending profile pictures for approval"""
    pending_users = get_pending_profile_pictures()
    return render_template("admin_profile_pictures.html", pending_users=pending_users)


@admin_bp.route("/profile-pictures/approve/<int:user_id>", methods=["POST"])
def approve_picture(user_id):
    """Approve a profile picture"""
    success, message = approve_profile_picture(user_id)
    flash(message)
    return redirect(url_for("admin.manage_profile_pictures"))


@admin_bp.route("/profile-pictures/reject/<int:user_id>", methods=["POST"])
def reject_picture(user_id):
    """Reject a profile picture"""
    success, message = reject_profile_picture(user_id)
    flash(message)
    return redirect(url_for("admin.manage_profile_pictures"))