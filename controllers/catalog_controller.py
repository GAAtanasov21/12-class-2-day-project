from flask import Blueprint, render_template, request
from services.catalog_service import list_products

catalog_bp = Blueprint("catalog", __name__, url_prefix="/catalog")

@catalog_bp.route("/")
def catalog():
    query = (request.args.get("q") or "").strip()
    color_filter = (request.args.get("color") or "").strip()
    products = list_products()
    return render_template("catalog.html", products=products, query=query, color_filter=color_filter)
