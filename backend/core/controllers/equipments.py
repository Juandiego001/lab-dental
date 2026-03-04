from flask_jwt_extended import jwt_required
from core.app import db
from core.services import equipments
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.equipments import EquipmentInUpdate, EquipmentInCreate, EquipmentOut, EquipmentSearch, EquipmentsOut
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
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
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
@bp.input(EquipmentInCreate, arg_name='equipment')
@jwt_required()
def create_equipments(equipment):
    '''Create equipments'''

    try:
        db.session.add(equipment)
        db.session.commit()
        return {'message': gettext('equipmentCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:equipment_id>')
@bp.input(EquipmentInUpdate)
@bp.output(Message)
@jwt_required()
def update_equipments(equipment_id, json_data):
    '''Update equipment'''

    try:
        db.session.merge(json_data)
        db.session.commit()
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
