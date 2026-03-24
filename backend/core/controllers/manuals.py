from flask_babel import gettext
from core.services import manuals
from core.schemas.utils import Message
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.manuals import (
    ManualOut,
    ManualsCreateIn,
    ManualsIn,
    ManualsOut,
    ManualsSearch,
    ManualTypesSearch,
    ManualTypesOut
)


bp = APIBlueprint('manuals', __name__)


@bp.post('/search')
@jwt_required()
@bp.input(ManualsSearch)
@bp.output(ManualsOut)
def search_manuals(json_data: dict):
    '''Search manuals'''

    try:
        items, total = manuals.search_manuals(
            equipment_id=json_data['equipment_id'],
            title=json_data['title'],
            description=json_data['description'],
            manual_type_id=json_data['manual_type_id'],
            original_name=json_data['original_name'],
            extension=json_data['extension'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'],
        )
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('')
@jwt_required()
@bp.input(ManualsCreateIn, location='form_and_files')
@bp.output(Message)
def create_manuals(form_and_files_data: dict):
    '''Create manuals'''

    try:
        manuals.create_manual(form_and_files_data)
        return {'message': gettext('manualCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:manual_id>')
@jwt_required()
@bp.output(ManualOut)
def get_manual(manual_id: int):
    '''Get manual'''

    try:
        return manuals.get_manual(
            manual_id=manual_id
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:manual_id>')
@jwt_required()
@bp.input(ManualsIn)
@bp.output(Message)
def update_manual(manual_id: int, json_data: dict):
    '''Update Manual'''

    try:
        manuals.update_manual(
            manual_id=manual_id,
            data=json_data
        )
        return {'message': gettext('manualUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:manual_id>')
@jwt_required()
@bp.output(Message)
def delete_manual(manual_id: int):
    '''Delete Manual'''

    try:
        manuals.delete_manual(manual_id)
        return {'message': gettext('manualDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/types/search')
@jwt_required()
@bp.input(ManualTypesSearch)
@bp.output(ManualTypesOut)
def search_manual_types(json_data: dict):
    '''Search manual types'''

    try:
        items, total = manuals.search_manual_types(
            name=json_data['name'],
            slug=json_data['slug'],
            page=json_data['page'],
            per_page=json_data['per_page']
        )
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))
