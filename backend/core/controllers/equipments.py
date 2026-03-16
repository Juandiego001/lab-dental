from flask_jwt_extended import jwt_required
from core.app import db
from core.services import equipments
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message
from core.schemas.equipments import EquipmentInUpdate, EquipmentInCreate, EquipmentOut, EquipmentSearch, EquipmentsOut, EquipmentFilesOut
from flask_babel import gettext


bp = APIBlueprint('equipments', __name__)


@bp.post('/search')
@bp.input(EquipmentSearch)
@bp.output(EquipmentsOut)
@jwt_required()
def search_equipments(json_data):
    '''Search equipments'''

    try:
        results, total = equipments.search_equipments(
            equipment_id=json_data['equipment_id'],
            brand_id=json_data['brand_id'],
            category_id=json_data['category_id'],
            model=json_data['model'],
            reference=json_data['reference'],
            with_picture=json_data['with_picture'],
            model_reference=json_data['model_reference'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        print(results)
        return {'items': results, 'total': total}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.get('/<int:equipment_id>')
@bp.output(EquipmentOut)
@jwt_required()
def get_equipment(equipment_id):
    '''Get equipment'''

    try:
        return equipments.get_equipment_by_id(equipment_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(EquipmentInCreate, location='form_and_files')
@jwt_required()
def create_equipments(form_and_files_data):
    '''Create equipments'''

    try:
        equipments.create_equipment(form_and_files_data)
        return {'message': gettext('equipmentCreated')}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.put('/<int:equipment_id>')
@bp.input(EquipmentInUpdate, location='form_and_files')
@bp.output(Message)
@jwt_required()
def update_equipments(equipment_id: int, form_and_files_data: dict):
    '''Update equipment'''

    try:
        equipments.update_equipment(
            equipment_id=equipment_id,
            equipment_data=form_and_files_data
        )
        return {'message': gettext('equipmentUpdated')}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.delete('/<int:equipment_id>')
@bp.output(Message)
@jwt_required()
def delete_equipments(equipment_id):
    '''Delete equipments'''

    try:
        equipments.delete_equipment(equipment_id)
        return {'message': gettext('equipmentDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:equipment_id>/files')
@jwt_required()
@bp.output(EquipmentFilesOut)
def get_media(equipment_id: int):
    '''Get files of an equipment'''

    try:
        return equipments.get_equipment_files(equipment_id=equipment_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.delete('/files/<int:equipment_file_id>')
@jwt_required()
@bp.output(Message)
def delete_equipment_file(equipment_file_id: int):
    '''Delete equipment file'''

    try:
        equipments.remove_equipment_file(equipment_file_id=equipment_file_id)
        return {'message': gettext('equipmentFileDeleted')}
    except Exception as ex:
        abort(500, str(ex))