from gogglekaap.models.memo import Memo as MemoModel
from gogglekaap.models.user import User as UserModel 
from flask_restx import Namespace, fields, Resource, reqparse
from flask import g

ns = Namespace(
    'memos',
    description='메모 관련 API'
)

memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='메모 고유 아이디'),
    'user_id': fields.Integer(required=True, description='유저 고유 아이디'),
    'title': fields.String(required=True, description='메모 제목'),
    'content': fields.String(required=True, description='메모 내용'),
    'created_at': fields.DateTime(description='메모 작성일'),
    'updated_at': fields.DateTime(description='메모 변경일'),
})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='메모 제목')
parser.add_argument('content', required=True, help='메모 내용')

@ns.route('')
class MemoList(Resource):

    @ns.marshal_list_with(memo, skip_none=True)
    def get(self):
        '''메모 복수 조회'''
        data = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id
        ).order_by(
            MemoModel.created_at.desc()
        ).limit(10).all()
        return data

    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(parser)
    def post(self):
        '''메모 생성'''
        args = parser.parse_args()
        memo = MemoModel(
            title=args['title'],
            content=args['content'],
            user_id=g.user.id
        )
        g.db.add(memo)
        g.db.commit()
        return memo, 201

@ns.param('id', '메모 고유 아이디')
@ns.route('/<int:id>')
class Memo(Resource):
    
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        '''메모 단수 조회'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        return memo