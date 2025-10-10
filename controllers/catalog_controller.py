from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from services.catalog_service import list_products, get_product, get_product_category
from services.review_service import create_review, get_product_reviews, user_has_reviewed

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")


@catalog_bp.route("/")
def catalog():
    # Get all query parameters
    query = (request.args.get("q") or "").strip()
    color_filter = (request.args.get("color") or "").strip()
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    size = request.args.get("size")
    in_stock = request.args.get("in_stock") == "on"
    category = request.args.get("category")
    sort_by = request.args.get("sort_by")

    # Convert to appropriate types
    min_price = float(min_price) if min_price else None
    max_price = float(max_price) if max_price else None
    size = int(size) if size and size.isdigit() else None

    # Get filtered and sorted products from database
    products = list_products(
        query=query,
        color=color_filter,
        min_price=min_price,
        max_price=max_price,
        size=size,
        in_stock=in_stock,
        category=category,
        sort_by=sort_by,
    )

    # Category display names
    category_names = {
        'running': 'Running Shoes',
        'everyday': 'Everyday Shoes',
        'official': 'Official Shoes',
        'mountain': 'Mountain Shoes'
    }
    category_display = category_names.get(category, "All Products")

    return render_template(
        "catalog.html",
        products=products,
        query=query,
        color_filter=color_filter,
        min_price=min_price or "",
        max_price=max_price or "",
        size=size or "",
        in_stock=in_stock,
        category=category,
        category_display=category_display,
        sort_by=sort_by or "",
    )


@catalog_bp.route("/categories")
def categories():
    return render_template("categories.html")


@catalog_bp.route("/product/<int:product_id>", methods=["GET", "POST"])
def product_detail(product_id):
    """Product detail page with reviews and ratings"""
    product = get_product(product_id)

    if not product:
        flash("Product not found")
        return redirect(url_for("catalog.catalog"))

    # Handle review submission
    if request.method == "POST":
        if not session.get("user_id"):
            flash("You must be logged in to leave a review")
            return redirect(url_for("auth.login"))

        user_id = session.get("user_id")
        rating = request.form.get("rating")
        comment = request.form.get("comment", "").strip()

        if not rating:
            flash("Please select a rating")
            return redirect(url_for("catalog.product_detail", product_id=product_id))

        if not comment:
            flash("Please write a comment")
            return redirect(url_for("catalog.product_detail", product_id=product_id))

        # Check if user already reviewed
        if user_has_reviewed(user_id, product_id):
            flash("You have already reviewed this product")
            return redirect(url_for("catalog.product_detail", product_id=product_id))

        # Create review
        create_review(user_id, product_id, int(rating), comment)
        flash("Thank you for your review!")
        return redirect(url_for("catalog.product_detail", product_id=product_id))

    # Get product details
    category = get_product_category(product)
    reviews = get_product_reviews(product_id)
    average_rating = product.get_average_rating()
    rating_count = product.get_rating_count()

    # Check if current user has reviewed
    user_has_reviewed_product = False
    if session.get("user_id"):
        user_has_reviewed_product = user_has_reviewed(session.get("user_id"), product_id)

    return render_template(
        "product_detail.html",
        product=product,
        category=category,
        reviews=reviews,
        average_rating=average_rating,
        rating_count=rating_count,
        user_has_reviewed=user_has_reviewed_product
    )