from core.services import groups
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from flask_jwt_extended import jwt_required, current_user
from core.schemas.groups import GroupInUpdate, GroupInCreate, GroupOut, GroupSearch, GroupsOut
from flask_babel import gettext


bp = APIBlueprint('groups', __name__)


@bp.post('/search')
@bp.input(GroupSearch)
@bp.output(GroupsOut)
@jwt_required()
def search_groups(json_data):
    '''Search groups'''

    try:
        results, total = groups.search_groups(
            current_user=current_user,
            distributor_id=json_data['distributor_id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:group_id>')
@bp.output(GroupOut)
@jwt_required()
def get_group(group_id):
    '''Get group'''

    try:
        return groups.get_group_by_id(group_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(GroupInCreate)
@bp.output(Message)
@jwt_required()
def create_groups(json_data):
    '''Create groups'''

    try:
        group_object, users_ids = json_data
        groups.create_group(current_user, group_object, users_ids)
        return {'message': gettext('groupCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:group_id>')
@bp.input(GroupInUpdate)
@bp.output(Message)
@jwt_required()
def update_groups(group_id, json_data):
    '''Update group'''

    try:
        groups.update_group(group_id, json_data)
        return {'message': gettext('groupUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:group_id>')
@bp.output(Message)
@jwt_required()
def delete_groups(group_id):
    '''Delete groups'''

    try:
        groups.delete_group(group_id)
        return {'message': gettext('groupDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
