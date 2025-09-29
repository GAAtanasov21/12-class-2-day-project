from flask import Blueprint, render_template, request
from services.catalog_service import list_products

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")

@catalog_bp.route("/")
def catalog():
    query = (request.args.get("q") or "").strip()
    color_filter = (request.args.get("color") or "").strip()
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    size = request.args.get("size")
    in_stock = request.args.get("in_stock") == "on"
    category = request.args.get("category")

    min_price = float(min_price) if min_price else None
    max_price = float(max_price) if max_price else None
    size = int(size) if size and size.isdigit() else None

    products = list_products(
        query=query,
        color=color_filter,
        min_price=min_price,
        max_price=max_price,
        size=size,
        in_stock=in_stock,
        category=category,
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
    )

@catalog_bp.route("/categories")
def categories():
    return render_template("categories.html")