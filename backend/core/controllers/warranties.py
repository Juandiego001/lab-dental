from flask_babel import gettext
from core.services import warranties
from apiflask import APIBlueprint, abort
from flask_jwt_extended import current_user, jwt_required
from core.schemas.utils import Message, Pagination
from core.schemas.warranties import WarrantyInUpdate, WarrantyInCreate, WarrantyOut, WarrantiesOut, WarrantySearch


bp = APIBlueprint('warranties', __name__)


@bp.post('/search')
@bp.input(WarrantySearch)
@bp.output(WarrantiesOut)
@jwt_required()
def get_warranties(json_data):
    '''Get warranties'''

    try:
        results, total = warranties.get_warranties(
            current_user=current_user,
            distributor_id=json_data['distributor_id'],
            equipment_id=json_data['equipment_id'],
            sale_date=json_data['sale_date'],
            invoice=json_data['invoice'],
            status=json_data['status'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by']
        )
        return {'items': results, 'total': total}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.get('/<int:warranty_id>')
@bp.output(WarrantyOut)
@jwt_required()
def get_warranty(warranty_id):
    '''Get warranty'''

    try:
        return warranties.get_warranty_by_id(warranty_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('')
@bp.input(WarrantyInCreate, arg_name='warranty')
@jwt_required()
def create_warranties(warranty: dict):
    '''Create warranties'''

    try:
        warranties.create_warranty(warranty)
        return {'message': gettext('warrantyCreated')}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.put('/<int:warranty_id>')
@bp.input(WarrantyInUpdate)
@bp.output(Message)
@jwt_required()
def update_warranties(warranty_id, json_data):
    '''Update warranties'''
    try:
        warranties.update_warranty(warranty_id, json_data)
        return {'message': gettext('warrantyUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:warranty_id>')
@bp.output(Message)
@jwt_required()
def delete_warranties(warranty_id):
    '''Delete warranties'''

    try:
        warranties.delete_warranty(warranty_id)
        return {'message': gettext('warrantyDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
