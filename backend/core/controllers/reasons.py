from flask_jwt_extended import jwt_required
from core.app import db
from core.services import reasons
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.reasons import ReasonInUpdate, ReasonInCreate, ReasonOut, ReasonsOut


bp = APIBlueprint('reasons', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ReasonsOut)
@jwt_required()
def get_reasons(query_data):
    '''Get reasons'''

    try:
        results = reasons.get_reasons(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:reason_id>')
@bp.output(ReasonOut)
@jwt_required()
def get_reason(reason_id):
    '''Get reason'''

    try:
        return reasons.get_reason_by_id(reason_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ReasonInCreate, arg_name='reason')
@jwt_required()
def create_reasons(reason):
    '''Create reasons'''

    try:
        db.session.add(reason)
        db.session.commit()
        return {'message': 'Reason registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:reason_id>')
@bp.input(ReasonInUpdate)
@bp.output(Message)
@jwt_required()
def update_reasons(reason_id, json_data):
    '''Update reason'''

    try:
        reasons.update_reason(reason_id, json_data)
        return {'message': 'Reason updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:reason_id>')
@bp.output(Message)
@jwt_required()
def delete_reasons(reason_id):
    '''Delete reasons'''

    try:
        reasons.delete_reason(reason_id)
        return {'message': 'Reason deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
