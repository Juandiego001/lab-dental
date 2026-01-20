from flask_jwt_extended import jwt_required
from core.app import db
from core.services import lists
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.lists import ListIn, ListOut, ListsOut


bp = APIBlueprint('lists', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ListsOut)
@jwt_required()
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
@jwt_required()
def get_list(list_id):
    '''Get list'''

    try:
        list_ = lists.get_list_by_id(list_id)

        if list_:
            list_ = list_._asdict()

            # Distributors ids unique validation
            list_['distributors_ids'] = list(set(list_['distributors_ids']))

            # Users ids not null validation
            list_['users_ids'] = [
                user_id for user_id in list_['users_ids'] if user_id]

            # If there is no user_id in the users_ids list, delete the key users_ids
            if len(list_['users_ids']) == 0:
                del list_['users_ids']
            else:
                list_['users_ids'] = list(set(list_['users_ids']))

        return list_
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ListIn, arg_name='list_')
@jwt_required()
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
@jwt_required()
def update_list(list_id, json_data):
    '''Update list'''

    try:
        lists.update_list(list_id, json_data)
        return {'message': 'List updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:list_id>')
@bp.output(Message)
@jwt_required()
def delete_list(list_id):
    '''Delete list'''

    try:
        lists.delete_list(list_id)
        return {'message': 'List deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
