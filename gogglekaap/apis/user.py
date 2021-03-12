from flask_restx import Namespace, Resource, fields, reqparse
from flask import g
from gogglekaap.models.user import User as UserModel
from werkzeug import security

ns = Namespace(
    'users',
    description='유저 관련 API'
)

user = ns.model('User', {
    'id': fields.Integer(required=True, description='유저 고유 아이디'),
    'user_id': fields.String(required=True, description='유저 아이디'),
    'user_name': fields.String(required=True, description='유저 이름'),
    'created_at': fields.DateTime(description='가입일자')
})

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', required=True, help='유저 고유 아이디')
post_parser.add_argument('user_name', required=True, help='유저 이름')
post_parser.add_argument('password', required=True, help='유저 패스워드')

@ns.route('')
@ns.response(409, 'User id is already exists.')
@ns.deprecated
class UserList(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        """유저 복수 조회"""
        data = UserModel.query.all()
        return data

    @ns.expect(post_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        """유저 생성"""
        args = post_parser.parse_args()
        user_id = args['user_id']
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            ns.abort(409)
        user = UserModel(
            user_id=user_id,
            user_name=args['user_name'],
            password=security.generate_password_hash(args['password'])
        )
        g.db.add(user)
        g.db.commit()
        return user, 201


@ns.route('/<int:id>')
@ns.param('id', '유저 고유 번호')
@ns.deprecated
class User(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        """유저 단수 조회"""
        data = UserModel.query.get_or_404(id)
        return data
