from flask_babel import gettext
from core.services import equipments
from core.schemas.utils import Message
from apiflask import APIBlueprint, abort
from flask_jwt_extended import current_user, jwt_required
from core.schemas.equipments import (
    EquipmentIn,
    EquipmentOut,
    EquipmentSearch,
    EquipmentsOut,
    EquipmentFilesOut,
    EquipmentFilesSearch,
    EquipmentFilesIn,
    EquipmentFileOut,
    EquipmentFileIn,
    EquipmentFileOrderIn,
)


bp = APIBlueprint('equipments', __name__)


@bp.post('/search')
@jwt_required()
@bp.input(EquipmentSearch)
@bp.output(EquipmentsOut)
def search_equipments(json_data):
    '''Search equipments'''

    try:
        items, total = equipments.search_equipments(
            current_user=current_user,
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
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:equipment_id>')
@jwt_required()
@bp.output(EquipmentOut)
def get_equipment(equipment_id):
    '''Get equipment'''

    try:
        return equipments.get_equipment_by_id(equipment_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(EquipmentIn)
@jwt_required()
def create_equipments(json_data: dict):
    '''Create equipments'''

    try:
        equipments.create_equipment(json_data)
        return {'message': gettext('equipmentCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:equipment_id>')
@bp.input(EquipmentIn)
@bp.output(Message)
@jwt_required()
def update_equipments(equipment_id: int, json_data: dict):
    '''Update equipment'''

    try:
        equipments.update_equipment(
            equipment_id=equipment_id,
            equipment_data=json_data
        )
        return {'message': gettext('equipmentUpdated')}
    except Exception as ex:
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


@bp.post('/<int:equipment_id>/files/search')
@jwt_required()
@bp.input(EquipmentFilesSearch)
@bp.output(EquipmentFilesOut)
def get_equipment_files(equipment_id: int, json_data: dict):
    '''Search files of an equipment'''

    try:
        items, total = equipments.search_equipment_files(
            equipment_id=equipment_id,
            title=json_data['title'],
            description=json_data['description'],
            original_name=json_data['original_name'],
            extension=json_data['extension'],
            page=json_data['page'],
            per_page=json_data['per_page']
        )
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/<int:equipment_id>/files')
@jwt_required()
@bp.input(EquipmentFilesIn, location='form_and_files')
@bp.output(Message)
def add_equipment_files(equipment_id: int, form_and_files_data: dict):
    '''Add equipment files'''

    try:
        equipments.add_files(
            equipment_id=equipment_id,
            files=form_and_files_data['files']
        )
        return {'message': gettext('equipmentFilesAdded')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/files/<int:file_id>')
@jwt_required()
@bp.output(EquipmentFileOut)
def get_equipment_file(file_id: int):
    '''Get equipment file'''

    try:
        return equipments.get_equipment_file(
            file_id=file_id
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/files/<int:file_id>')
@jwt_required()
@bp.input(EquipmentFileIn)
@bp.output(Message)
def update_equipment_file(file_id: int, json_data: dict):
    '''Update Equipment File'''

    try:
        equipments.update_equipment_file(
            file_id=file_id,
            data=json_data
        )
        return {'message': gettext('equipmentFileUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:equipment_id>/files/<int:file_id>/order')
@jwt_required()
@bp.input(EquipmentFileOrderIn)
@bp.output(Message)
def update_equipment_file_order(equipment_id: int, file_id: int, json_data: dict):
    '''Update equipment file order'''

    try:
        equipments.update_equipment_file_order(
            equipment_id=equipment_id,
            file_id=file_id,
            new_sort_order=json_data['new_sort_order']
        )
        return {'message': gettext('equipmentFileOrderUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/files/<int:equipment_file_id>')
@jwt_required()
@bp.output(Message)
def delete_equipment_file(equipment_file_id: int):
    '''Delete equipment file'''

    try:
        equipments.remove_equipment_file(equipment_file_id=equipment_file_id)
        return {'message': gettext('equipmentFileDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
