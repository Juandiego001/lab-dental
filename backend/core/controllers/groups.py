from core.app import db
from core.services import groups
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.groups import GroupInUpdate, GroupInCreate, GroupOut, GroupsOut


bp = APIBlueprint('groups', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(GroupsOut)
def get_groups(query_data):
    '''Get groups'''

    try:
        return {'items': groups.get_groups(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:group_id>')
@bp.output(GroupOut)
def get_group(group_id):
    '''Get group'''

    try:
        return groups.get_group_by_id(group_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(GroupInCreate, arg_name='group')
def create_groups(group):
    '''Create groups'''

    try:
        db.session.add(group)
        db.session.commit()
        return {'message': 'Group registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:group_id>')
@bp.input(GroupInUpdate)
@bp.output(Message)
def update_groups(group_id, json_data):
    '''Update group'''

    try:
        groups.update_group(group_id, json_data)
        return {'message': 'Group updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:group_id>')
@bp.output(Message)
def delete_groups(group_id):
    '''Delete groups'''

    try:
        groups.delete_group(group_id)
        return {'message': 'Group deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
