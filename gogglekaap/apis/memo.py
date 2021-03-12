from gogglekaap.models.memo import Memo as MemoModel
from flask_restx import Namespace

ns = Namespace(
    'memos',
    description='메모 관련 API'
)
