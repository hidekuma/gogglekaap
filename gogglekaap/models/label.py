from gogglekaap import db
from sqlalchemy import func

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10), unique=False, nullable=False)
    created_at = db.Column(
        db.DateTime(),
        default=func.now()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    __table_args__ = (
        db.UniqueConstraint(
            "content",
            "user_id",
            name="uk_content_user_id"
        ),
    )
