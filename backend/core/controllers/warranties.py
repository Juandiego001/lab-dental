from flask_jwt_extended import jwt_required
from core.app import db
from core.services import warranties
from apiflask import APIBlueprint, abort
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message, Pagination
from core.schemas.warranties import WarrantyInUpdate, WarrantyInCreate, WarrantyOut, WarrantiesOut


bp = APIBlueprint('warranties', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(WarrantiesOut)
@jwt_required()
def get_warranties(query_data):
    '''Get warranties'''

    try:
        results = warranties.get_warranties(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:warranty_id>')
@bp.output(WarrantyOut)
@jwt_required()
def get_warranty(warranty_id):
    '''Get warranty'''

    try:
        return warranties.get_warranty_by_id(warranty_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(WarrantyInCreate, arg_name='warranty')
@jwt_required()
def create_warranties(warranty):
    '''Create warranties'''

    try:
        db.session.add(warranty)
        db.session.commit()
        return {'message': 'warranty registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:warranty_id>')
@bp.input(WarrantyInUpdate)
@bp.output(Message)
@jwt_required()
def update_warranties(warranty_id, json_data):
    '''Update warranties'''
    try:
        warranties.update_warranty(warranty_id, json_data)
        return {'message': 'Warranty updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:warranty_id>')
@bp.output(Message)
@jwt_required()
def delete_warranties(warranty_id):
    '''Delete warranties'''

    try:
        warranties.delete_warranty(warranty_id)
        return {'message': 'Warranty deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
