from core.app import db
from core.services import equipments
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.equipments import EquipmentInUpdate, EquipmentInCreate, EquipmentOut, EquipmentsOut


bp = APIBlueprint('equipments', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(EquipmentsOut)
def get_equipments(query_data):
    '''Get equipments'''

    try:
        results = equipments.get_equipments(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])

        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:equipment_id>')
@bp.output(EquipmentOut)
def get_equipment(equipment_id):
    '''Get equipment'''

    try:
        return equipments.get_equipment_by_id(equipment_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(EquipmentInCreate, arg_name='equipment')
def create_equipments(equipment):
    '''Create equipments'''

    try:
        db.session.add(equipment)
        db.session.commit()
        return {'message': 'Equipment registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:equipment_id>')
@bp.input(EquipmentInUpdate)
@bp.output(Message)
def update_equipments(equipment_id, json_data):
    '''Update equipment'''

    try:
        equipments.update_equipment(equipment_id, json_data)
        return {'message': 'Equipment updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:equipment_id>')
@bp.output(Message)
def delete_equipments(equipment_id):
    '''Delete equipments'''

    try:
        equipments.delete_equipment(equipment_id)
        return {'message': 'Equipment deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
