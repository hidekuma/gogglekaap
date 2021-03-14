from flask_restx import Namespace, fields
from gogglekaap.models.label import Label as LabelModel

ns = Namespace(
    'labels',
    description='라벨 관련 API'
)

label = ns.model('Label', {
    'id': fields.Integer(required=True, description='라벨 고유 아이디'),
    'user_id': fields.Integer(required=True, description='라벨 작성자 유저 고유 아이디'),
    'content': fields.String(required=True, description='라벨 내용'),
    'created_at': fields.DateTime(description='라벨 생성일자')
})
