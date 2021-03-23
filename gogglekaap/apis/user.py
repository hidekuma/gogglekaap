from flask_restx import Namespace, Resource, fields
from gogglekaap.models.user import User as UserModel


ns = Namespace(
    'users',
    description='유저 관련 API'
)

user = ns.model('User', {
    'id': fields.Integer(required=True, description="유저 고유 번호"),
    'user_id': fields.String(required=True, description='유저 아이디'),
    'user_name': fields.String(required=True, description='유저 이름')
})


@ns.route('')
class UserList(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        """유저 복수 조회"""
        return UserModel.query.all()


@ns.route('/<int:id>')
@ns.param('id', description='유저 고유 번호')
class User(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        """유저 단수 조회"""
        return UserModel.query.get_or_404(id)
