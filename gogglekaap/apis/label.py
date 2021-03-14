from flask import g
from flask_restx import Namespace, Resource, fields, reqparse
from gogglekaap.models.label import Label as LabelModel
from gogglekaap.models.user import User as UserModel

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

parser = reqparse.RequestParser()
parser.add_argument('content', required=True, type=str, help="라벨 내용")


@ns.route('')
class LabelList(Resource):
    @ns.marshal_list_with(label, skip_none=True)
    def get(self):
        '''라벨 복수 조회'''
        pages = LabelModel.query.join(
            UserModel,
            UserModel.id == LabelModel.user_id
        ).filter(
            UserModel.id == g.user.id,
        )
        return pages.all()

    @ns.marshal_list_with(label, skip_none=True)
    @ns.expect(parser)
    def post(self):
        '''라벨 생성'''
        args = parser.parse_args()
        content = args['content']
        label = LabelModel.query.join(
            UserModel,
            UserModel.id == LabelModel.user_id
        ).filter(
            UserModel.id == g.user.id,
            LabelModel.content == content
        ).first()

        if label:
            ns.abort(409)

        label = LabelModel(
            content=content,
            user_id=g.user.id
        )
        g.db.add(label)
        g.db.commit()
        return label, 201

@ns.route('/<id>')
@ns.param('id', '라벨 고유 번호')
class Label(Resource):
    def delete(self, id):
        '''라벨 삭제'''
        label = LabelModel.query.get_or_404(id)
        if label.user_id != g.user.id:
            ns.abort(403)
        g.db.delete(label)
        g.db.commit()
        return '', 204
