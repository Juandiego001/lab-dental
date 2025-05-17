from core.app import db
from core.services import manuals
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.manuals import ManualInUpdate, ManualInCreate, ManualOut, ManualsOut


bp = APIBlueprint('manuals', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ManualsOut)
def get_manuals(query_data):
    '''Get manuals'''

    try:
        return {'items': manuals.get_manuals(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:manual_id>')
@bp.output(ManualOut)
def get_manual(manual_id):
    '''Get manual'''

    try:
        return manuals.get_manual_by_id(manual_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ManualInCreate, arg_name='manual')
def create_manuals(manual):
    '''Create manuals'''

    try:
        db.session.add(manual)
        db.session.commit()
        return {'message': 'Manual registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:manual_id>')
@bp.input(ManualInUpdate)
@bp.output(Message)
def update_manuals(manual_id, json_data):
    '''Update manuals'''
    try:
        manuals.update_manual(manual_id, json_data)
        return {'message': 'Manual updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:manual_id>')
@bp.output(Message)
def delete_manuals(manual_id):
    '''Delete manuals'''

    try:
        manuals.delete_manual(manual_id)
        return {'message': 'Manual deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
