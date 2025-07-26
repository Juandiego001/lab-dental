from flask_jwt_extended import jwt_required
from core.app import db
from core.services import parts
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.parts import PartInUpdate, PartInCreate, PartOut, PartsOut


bp = APIBlueprint('parts', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(PartsOut)
@jwt_required()
def get_parts(query_data):
    '''Get parts'''

    try:
        results = parts.get_parts(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:part_id>')
@bp.output(PartOut)
@jwt_required()
def get_part(part_id):
    '''Get part'''

    try:
        return parts.get_part_by_id(part_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(PartInCreate, arg_name='part')
@jwt_required()
def create_parts(part):
    '''Create parts'''

    try:
        db.session.add(part)
        db.session.commit()
        return {'message': 'Part registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:part_id>')
@bp.input(PartInUpdate)
@bp.output(Message)
@jwt_required()
def update_parts(part_id, json_data):
    '''Update part'''

    try:
        parts.update_part(part_id, json_data)
        return {'message': 'Part updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:part_id>')
@bp.output(Message)
@jwt_required()
def delete_parts(part_id):
    '''Delete parts'''

    try:
        parts.delete_part(part_id)
        return {'message': 'Part deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
