from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from services.order_service import get_user_orders
from services.auth_service import get_user_by_id

calendar_bp = Blueprint("calendar", __name__, url_prefix="/calendar")


@calendar_bp.route("/")
def view_calendar():
    """View calendar with orders"""
    if not session.get("user_id"):
        flash("Please login to view calendar")
        return redirect(url_for("auth.login"))

    user = get_user_by_id(session.get("user_id"))
    if not user:
        flash("User not found")
        return redirect(url_for("index"))

    # Get current month/year from query params or use current
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    now = datetime.now()
    if not year or not month:
        year = now.year
        month = now.month

    # Get user's orders
    orders = get_user_orders(user.id)

    return render_template("calendar.html",
                           user=user,
                           orders=orders,
                           current_year=year,
                           current_month=month,
                           today=now.date())


@calendar_bp.route("/api/orders")
def get_orders_json():
    """API endpoint to get orders as JSON for calendar"""
    if not session.get("user_id"):
        return jsonify({"error": "Not authenticated"}), 401

    user_id = session.get("user_id")
    orders = get_user_orders(user_id)

    # Convert orders to calendar events format
    events = []
    for order in orders:
        events.append({
            'id': order.id,
            'title': f'Order #{order.id} - ${order.total:.2f}',
            'start': order.created_at.strftime('%Y-%m-%d'),
            'url': url_for('calendar.order_details', order_id=order.id),
            'backgroundColor': '#2c3e50',
            'borderColor': '#2c3e50',
            'extendedProps': {
                'total': order.total,
                'items': len(order.items),
                'address': order.address
            }
        })

    return jsonify(events)


@calendar_bp.route("/order/<int:order_id>")
def order_details(order_id):
    """View detailed order information"""
    if not session.get("user_id"):
        flash("Please login")
        return redirect(url_for("auth.login"))

    from services.order_service import get_order
    order = get_order(order_id)

    if not order:
        flash("Order not found")
        return redirect(url_for("calendar.view_calendar"))

    # Check if order belongs to user
    if order.user_id != session.get("user_id"):
        flash("Access denied")
        return redirect(url_for("calendar.view_calendar"))

    return render_template("order_detail.html", order=order)