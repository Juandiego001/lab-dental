from core.services import groups
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from flask_jwt_extended import jwt_required, current_user
from core.schemas.groups import GroupInUpdate, GroupInCreate, GroupOut, GroupsOut


bp = APIBlueprint('groups', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(GroupsOut)
@jwt_required()
def get_groups(query_data):
    '''Get groups'''

    try:
        results, total = groups.get_groups(
            current_user,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:group_id>')
@bp.output(GroupOut)
@jwt_required()
def get_group(group_id):
    '''Get group'''

    try:
        return groups.get_group_by_id(group_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(GroupInCreate)
@bp.output(Message)
@jwt_required()
def create_groups(json_data):
    '''Create groups'''

    try:
        group_object, users_ids = json_data
        groups.create_group(current_user, group_object, users_ids)
        return {'message': 'Group registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:group_id>')
@bp.input(GroupInUpdate)
@bp.output(Message)
@jwt_required()
def update_groups(group_id, json_data):
    '''Update group'''

    try:
        groups.update_group(group_id, json_data)
        return {'message': 'Group updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:group_id>')
@bp.output(Message)
@jwt_required()
def delete_groups(group_id):
    '''Delete groups'''

    try:
        groups.delete_group(group_id)
        return {'message': 'Group deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
