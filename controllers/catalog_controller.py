# shoestore/controllers/catalog_controller.py
from flask import Blueprint, render_template, request
from services.catalog_service import list_products, init_sample_products

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")

@catalog_bp.route("/")
def catalog():
    init_sample_products()
    query = (request.args.get("q") or "").lower().strip()
    color_filter = (request.args.get("color") or "").lower().strip()

    products = list_products()

    if query:
        products = [p for p in products if query in p.name.lower() or query in p.color.lower()]
    if color_filter:
        products = [p for p in products if p.color.lower() == color_filter]

    return render_template("catalog.html", products=products, query=query, color_filter=color_filter)
