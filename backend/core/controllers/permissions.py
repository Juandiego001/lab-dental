from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.models import Permission
from core.schemas.permissions import PermissionIn, PermissionsGroupOut
from core.schemas.utils import Pagination
from core.services import permissions
from core.app import db


bp = APIBlueprint('permissions', __name__)


@bp.get('/')
@jwt_required()
def get_permissions():
    '''Get permissions'''
    pass


@bp.get('/groups/<int:group_id>')
@bp.input(Pagination, location='query')
@bp.output(PermissionsGroupOut)
@jwt_required()
def get_permissions_by_group_id(group_id: int, query_data):
    '''Get permissions by group_id'''

    try:
        results, total = permissions.get_permissions_by_group_id(
            current_user,
            group_id,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/')
@bp.input(PermissionIn)
@jwt_required()
def update_permissions(json_data):
    '''Update permissions'''

    try:
        permissions.update_permissions(json_data)
        return {'message': 'Permission updated succesfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
