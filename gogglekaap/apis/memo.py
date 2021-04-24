import os
import shutil
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from gogglekaap.models.memo import Memo as MemoModel
from gogglekaap.models.user import User as UserModel
from gogglekaap.models.label import Label as LabelModel
from flask_restx import Namespace, Resource, fields, reqparse, inputs
from flask import g, current_app

ns = Namespace(
    'memos',
    description='메모 관련 API'
)

label = ns.model('Label', {
    'id': fields.Integer(required=True, description='라벨 고유 아이디'),
    'content': fields.String(required=True, description='라벨 내용'),
})

memo = ns.model('Memo', {
    'id': fields.Integer(required=True, description='메모 고유 아이디'),
    'user_id': fields.Integer(required=True, description='메모 작성자 유저 고유 번호'),
    'title': fields.String(required=True, description='메모 제목'),
    'content': fields.String(required=True, description='메모 내용'),
    'linked_image': fields.String(required=False, description='메모 이미지'),
    'is_deleted': fields.Boolean(description='메모 삭제 상태'),
    'labels': fields.List(fields.Nested(label), description='연결된 라벨'),
    'created_at': fields.DateTime(description='작성일'),
    'updated_at': fields.DateTime(description='변경일')
})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='메모 제목')
parser.add_argument('content', required=True, help='메모 내용')
parser.add_argument('linked_image', location='files', type=FileStorage, required=False, help='메모 이미지')
parser.add_argument('is_deleted', required=False, type=inputs.boolean, help="메모 삭제 상태")
parser.add_argument('labels', action='split', help="라벨 내용 콤마 스트링")

put_parser = parser.copy()
put_parser.replace_argument('title', required=False, help='메모 제목')
put_parser.replace_argument('content', required=False, help='메모 내용')

get_parser = reqparse.RequestParser()
get_parser.add_argument('page', required=False, type=int, help='메모 페이지 번호')
get_parser.add_argument('needle', required=False, location='args', help='메모 검색어')
get_parser.add_argument('is_deleted', required=False, type=inputs.boolean, help="메모 삭제 상태")
get_parser.add_argument('label', required=False, help='라벨 내용')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {
            'jpg',
            'jpeg',
            'png',
            'gif'
        }

def randomword(length):
    import random, string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def save_file(file):
    if file.filename == '':
        ns.abort(400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        relative_path = os.path.join(
            current_app.static_url_path[1:],
            current_app.config['USER_STATIC_BASE_DIR'],
            g.user.user_id,
            'memos',
            randomword(10),
            filename
        )
        upload_path = os.path.join(
            current_app.root_path,
            relative_path
        )
        os.makedirs(
            os.path.dirname(upload_path),
            exist_ok=True
        )
        file.save(upload_path)
        return relative_path, upload_path
    else:
        ns.abort(400)

@ns.route("")
class MemoList(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    @ns.expect(get_parser)
    def get(self):
        '''메모 복수 조회'''
        args = get_parser.parse_args()
        needle = args['needle']
        page = args['page']
        per_page = 15
        is_deleted = args['is_deleted']
        label = args['label']
        if is_deleted is None:
            is_deleted = False
        base_query = MemoModel.query.join(
            UserModel,
            UserModel.id == MemoModel.user_id
        ).filter(
            UserModel.id == g.user.id,
            MemoModel.is_deleted == is_deleted
        )
        if needle:
            needle = f'%%{needle}%%'
            base_query = base_query.filter(
                MemoModel.title.ilike(needle)|MemoModel.content.ilike(needle)
            )
        if label:
            base_query = base_query.filter(
                MemoModel.labels.any(LabelModel.id == label)
            )

        pages = base_query.order_by(
            MemoModel.created_at.desc()
        ).paginate(
            per_page=per_page,
            page=page
        )
        return pages.items

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
        if args['is_deleted'] is not None:
            memo.is_deleted = args['is_deleted']
        file = args['linked_image']
        if file:
            relative_path, _ = save_file(file)
            memo.linked_image = relative_path
        labels = args['labels']
        if labels:
            for cnt in labels:
                if cnt:
                    label = LabelModel.query.filter(
                        LabelModel.content == cnt,
                        LabelModel.user_id == g.user.id
                    ).first()
                    if not label:
                        label = LabelModel(
                            content=cnt,
                            user_id=g.user.id
                        )
                    memo.labels.append(label)
        g.db.add(memo)
        g.db.commit()
        return memo, 201


@ns.param("id", '메모 고유 번호')
@ns.route("/<int:id>")
class Memo(Resource):
    @ns.marshal_list_with(memo, skip_none=True)
    def get(self, id):
        '''메모 단수 조회'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        return memo

    @ns.marshal_with(memo, skip_none=True)
    @ns.expect(put_parser)
    def put(self, id):
        '''메모 업데이트'''
        args = put_parser.parse_args()
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if args['title'] is not None:
            memo.title = args['title']
        if args['content'] is not None:
            memo.content = args['content']
        if args['is_deleted'] is not None:
            memo.is_deleted = args['is_deleted']
        file = args['linked_image']
        if file:
            relative_path, upload_path = save_file(file)
            if memo.linked_image:
                origin_path = os.path.join(
                    current_app.root_path,
                    memo.linked_image
                )
                if origin_path != upload_path:
                    if os.path.isfile(origin_path):
                        shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = relative_path
        labels = args['labels']
        if labels:
            memo.labels.clear()
            for cnt in labels:
                if cnt:
                    label = LabelModel.query.filter(
                        LabelModel.content == cnt,
                        LabelModel.user_id == g.user.id
                    ).first()
                    if not label:
                        label = LabelModel(
                            content=cnt,
                            user_id=g.user.id
                        )
                    memo.labels.append(label)


        g.db.commit()
        return memo

    def delete(self, id):
        '''메모 삭제'''
        memo = MemoModel.query.get_or_404(id)
        if memo.user_id != g.user.id:
            ns.abort(403)
        g.db.delete(memo)
        g.db.commit()
        return '', 204

@ns.route('/<id>/image')
@ns.param('id', 'The memo identifier')
class MemoImage(Resource):

    def delete(self, id):
        '''메모 이미지 삭제'''
        memo = MemoModel.query.get_or_404(id)
        if g.user.id != memo.user_id:
            ns.abort(403)
        if memo.linked_image:
            origin_path = os.path.join(
                current_app.root_path,
                memo.linked_image
            )
            if os.path.isfile(origin_path):
                shutil.rmtree(os.path.dirname(origin_path))
            memo.linked_image = None
            g.db.commit()
        return '', 204
