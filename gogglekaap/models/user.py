from gogglekaap import db
from sqlalchemy import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())

    @classmethod
    def find_one_by_user_id(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()
