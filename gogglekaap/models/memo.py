from gogglekaap import db
from sqlalchemy import func

memos_labels = db.Table('memos_labels',
    db.Column('memo_id', db.Integer, db.ForeignKey('memo.id'), primary_key=True),
    db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True)
)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    linked_image = db.Column(db.String(200), nullable=True)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(
        db.DateTime(),
        default=func.now()
    )
    updated_at = db.Column(
        db.DateTime(),
        default=func.now(),
        onupdate=func.now()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    labels = db.relationship(
        'Label',
        secondary=memos_labels,
        backref=db.backref('memos')
    )
