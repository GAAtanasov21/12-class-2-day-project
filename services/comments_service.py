from services.models import Comments, db


def get_comment(comment):
    """Get comment by ID"""
    return Comments.query.get(comment)

def create_comment(user_id, comment_text):
    """Create a new comment"""
    comment = Comments(
        user_id=user_id,
        comment=comment_text,
    )
    db.session.add(comment)
    db.session.commit()
    return comment
