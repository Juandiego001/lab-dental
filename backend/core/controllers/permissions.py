from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
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
            group_id,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/')
@bp.input(PermissionIn, arg_name='permission_obj')
@jwt_required()
def update_permissions_by_group_id(permission_obj: Permission):
    '''Update permissions by group_id'''

    try:
        db.session.merge(permission_obj)
        db.session.commit()
        return {'message': 'Permission updated succesfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.post('/')
@jwt_required()
def create_permissions():
    '''Create permissions'''
    pass


@bp.put('/')
@jwt_required()
def update_permissions():
    '''Update permissions'''
    pass


@bp.delete('/')
@jwt_required()
def delete_permissions():
    '''Delete permissions'''
    pass
