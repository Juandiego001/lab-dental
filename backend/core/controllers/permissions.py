from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.permissions import PermissionsGroupOut
from core.services import permissions


bp = APIBlueprint('permissions', __name__)


@bp.get('/')
def get_permissions():
    '''Get permissions'''
    pass


@bp.get('/groups/<int:group_id>')
@bp.output(PermissionsGroupOut)
@jwt_required()
def get_permissions_by_group_id(group_id: int):
    '''Get permissions by group_id'''

    try:
        results, total = permissions.get_permissions_by_group_id(group_id)
        return {'items': results, 'total': total}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.post('/')
def create_permissions():
    '''Create permissions'''
    pass


@bp.put('/')
def update_permissions():
    '''Update permissions'''
    pass


@bp.delete('/')
def delete_permissions():
    '''Delete permissions'''
    pass