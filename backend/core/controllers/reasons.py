from flask_babel import gettext
from flask_jwt_extended import jwt_required
from core.app import db
from core.models import Reason
from core.services import reasons
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.reasons import ReasonInUpdate, ReasonInCreate, ReasonOut, ReasonsOut, ReasonsSearch


bp = APIBlueprint('reasons', __name__)


@bp.post('/search')
@jwt_required()
@bp.input(ReasonsSearch)
@bp.output(ReasonsOut)
@jwt_required()
def search_reasons(json_data: dict):
    '''Search reasons'''

    try:
        items, total = reasons.search_reasons(
            reasons_ids=json_data['reasons_ids'],
            category_id=json_data['category_id'],
            name=json_data['name'],
            slug=json_data['slug'],
            description=json_data['description'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:reason_id>')
@bp.output(ReasonOut)
@jwt_required()
def get_reason(reason_id):
    '''Get reason'''

    try:
        return reasons.get_reason_by_id(reason_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('')
@bp.input(ReasonInCreate, arg_name='reason')
@jwt_required()
def create_reasons(reason: dict):
    '''Create reasons'''

    try:
        db.session.add(Reason(**reason))
        db.session.commit()
        return {'message': gettext('reasonCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:reason_id>')
@bp.input(ReasonInUpdate)
@bp.output(Message)
@jwt_required()
def update_reasons(reason_id: int, json_data: dict):
    '''Update reason'''

    try:
        reasons.update_reason(reason_id, json_data)
        return {'message': gettext('reasonUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:reason_id>')
@bp.output(Message)
@jwt_required()
def delete_reasons(reason_id):
    '''Delete reasons'''

    try:
        reasons.delete_reason(reason_id)
        return {'message': gettext('reasonDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
