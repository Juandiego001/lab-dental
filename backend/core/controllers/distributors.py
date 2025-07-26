from core.schemas.users import UsersOut
from core.services import distributors
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.clients import ClientsOut
from flask_jwt_extended import current_user
from core.schemas.utils import Message, Pagination
from core.schemas.distributors import DistributorInUpdate, DistributorInCreate, DistributorOut, DistributorsOut


bp = APIBlueprint('distributors', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(DistributorsOut)
@jwt_required()
def get_distributors(query_data):
    '''Get distributors'''

    try:
        results = distributors.get_distributors(
            current_user,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:distributor_id>')
@bp.output(DistributorOut)
@jwt_required()
def get_distributor(distributor_id):
    '''Get distributor'''

    try:
        return distributors.get_distributor_by_id(distributor_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:distributor_id>/clients')
@bp.input(Pagination, location='query')
@bp.output(ClientsOut)
@jwt_required()
def get_clients_by_distributor(distributor_id, query_data):
    '''Get clients of a distributor'''

    try:
        return distributors.get_clients_by_distributor_id(distributor_id,
                                                          query_data['search'])
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:distributor_id>/users')
@bp.input(Pagination, location='query')
@bp.output(UsersOut)
@jwt_required()
def get_users_by_distributor(distributor_id, query_data):
    '''Get users of a distributor'''

    try:
        return distributors.get_users_by_distributor_id(distributor_id,
                                                        query_data['search'])
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/distributors/users')
@bp.input(Pagination, location='query')
@bp.output(DistributorsOut)
@jwt_required()
def get_distributors_for_users_creation(query_data):
    '''Get distributors for users creation without Snapon distributor'''

    try:
        return distributors.get_distributors_for_users_creation(current_user, query_data['search'])
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(DistributorInCreate, arg_name='distributor')
@jwt_required()
def create_distributors(distributor):
    '''Create distributors'''

    try:
        distributors.create_distributor(distributor)
        return {'message': 'Distributor registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:distributor_id>')
@bp.input(DistributorInUpdate)
@bp.output(Message)
@jwt_required()
def update_distributors(distributor_id, json_data):
    '''Update distributor'''
    try:
        distributors.update_distributor(distributor_id, json_data)
        return {'message': 'Distributor updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:distributor_id>')
@bp.output(Message)
@jwt_required()
def delete_distributors(distributor_id):
    '''Delete distributors'''

    try:
        distributors.delete_distributor(distributor_id)
        return {'message': 'Distributor deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
