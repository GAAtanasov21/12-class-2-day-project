from services.models import db, ProductReview


def create_review(user_id, product_id, rating, comment):
    """Create a new product review"""
    review = ProductReview(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return review


def get_product_reviews(product_id):
    """Get all reviews for a product, ordered by newest first"""
    return ProductReview.query.filter_by(product_id=product_id).order_by(
        ProductReview.created_at.desc()
    ).all()


def get_user_reviews(user_id):
    """Get all reviews by a user"""
    return ProductReview.query.filter_by(user_id=user_id).order_by(
        ProductReview.created_at.desc()
    ).all()


def user_has_reviewed(user_id, product_id):
    """Check if user has already reviewed a product"""
    existing_review = ProductReview.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()
    return existing_review is not None


def delete_review(review_id):
    """Delete a review"""
    review = ProductReview.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False


def get_review(review_id):
    """Get a specific review"""
    return ProductReview.query.get(review_id)