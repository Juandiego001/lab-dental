from core.app import db
from core.services import lists
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.lists import ListIn, ListOut, ListsOut


bp = APIBlueprint('lists', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ListsOut)
def get_lists(query_data):
    '''Get lists'''

    try:
        results = lists.get_lists(query_data['search'],
                                  query_data['page'],
                                  query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:list_id>')
@bp.output(ListOut)
def get_list(list_id):
    '''Get list'''

    try:
        return lists.get_list_by_id(list_id)  
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ListIn, arg_name='list_')
def create_list(list_):
    '''Create list'''

    try:
        lists.create_list(list_)
        return {'message': 'List created successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:list_id>')
@bp.input(ListIn)
@bp.output(Message)
def update_list(list_id, json_data):
    '''Update list'''

    try:
        lists.update_list(list_id, json_data)
        return {'message': 'List updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:list_id>')
@bp.output(Message)
def delete_list(list_id):
    '''Delete list'''

    try:
        lists.delete_list(list_id)
        return {'message': 'List deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
