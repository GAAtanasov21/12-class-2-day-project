import datetime

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from services.comments_service import *
comments_bp = Blueprint("comments", __name__, url_prefix="/catalog")
@comments_bp.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "POST":
        user_id = session.get("user_id")
        comment_text = request.form.get("c")
        if user_id and comment_text:
            create_comment(user_id, comment_text)

    all_comments = Comments.query.order_by(Comments.created_at.desc()).all()
    return render_template("comments.html", comments=all_comments)


