from flask_jwt_extended import jwt_required
from core.app import db
from core.schemas.distributors import DistributorsExistingIn, DistributorsOut
from core.schemas.users import UsersExistingIn, UsersOut
from core.services import lists
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.lists import ListIn, ListOut, ListsOut
from flask_babel import gettext


bp = APIBlueprint('lists', __name__)


@bp.post('/search')
@bp.input(Pagination)
@bp.output(ListsOut)
@jwt_required()
def get_lists(json_data):
    '''Get lists'''

    try:
        results = lists.get_lists(json_data['search'],
                                  json_data['page'],
                                  json_data['per_page'],
                                  json_data['sort_by'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, gettext('abortException'))


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
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(ListIn, arg_name='list_')
@jwt_required()
def create_list(list_):
    '''Create list'''

    try:
        lists.create_list(list_)
        return {'message': gettext('listCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:list_id>')
@bp.input(ListIn)
@bp.output(Message)
@jwt_required()
def update_list(list_id, json_data):
    '''Update list'''

    try:
        lists.update_list(list_id, json_data)
        return {'message': gettext('listUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/distributors')
@bp.input(DistributorsExistingIn)
@bp.output(DistributorsOut)
@jwt_required()
def get_distributors_for_lists(json_data):
    '''Get distributors with existing distributors for lists'''

    try:
        return lists.get_distributors_and_existing(
            json_data['search'] if 'search' in json_data else '',
            json_data['distributors_ids'] if 'distributors_ids' in json_data else []
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:list_id>')
@bp.output(Message)
@jwt_required()
def delete_list(list_id):
    '''Delete list'''

    try:
        lists.delete_list(list_id)
        return {'message': gettext('listDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/users')
@bp.input(UsersExistingIn)
@bp.output(UsersOut)
@jwt_required()
def get_users(json_data):
    '''Get users of a list for autocomplete. Existing users and new ones'''

    try:
        return lists.get_users_and_existing(
            json_data['search'] if 'search' in json_data else '',
            json_data['users_ids'] if 'users_ids' in json_data else [])
    except Exception as ex:
        abort(500, gettext('abortException'))
