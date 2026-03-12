from core.services import distributors
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.schemas.clients import ClientsOut
from core.schemas.utils import Message, Pagination
from core.schemas.distributors import DistributorInUpdate, DistributorInCreate, DistributorOut, DistributorSearch, DistributorsOut
from flask_babel import gettext


bp = APIBlueprint('distributors', __name__)


@bp.post('/search')
@bp.input(DistributorSearch)
@bp.output(DistributorsOut)
@jwt_required()
def search_distributors(json_data):
    '''Search distributors'''

    try:
        results, total = distributors.search_distributors(
            current_user=current_user,
            distributors_ids=json_data['distributors_ids'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:distributor_id>')
@bp.output(DistributorOut)
@jwt_required()
def get_distributor(distributor_id):
    '''Get distributor'''

    try:
        return distributors.get_distributor_by_id(distributor_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


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
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(DistributorInCreate, arg_name='distributor')
@jwt_required()
def create_distributors(distributor):
    '''Create distributors'''

    try:
        distributors.create_distributor(distributor)
        return {'message': gettext('distributorCreated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.put('/<int:distributor_id>')
@bp.input(DistributorInUpdate)
@bp.output(Message)
@jwt_required()
def update_distributors(distributor_id, json_data):
    '''Update distributor'''
    try:
        distributors.update_distributor(distributor_id, json_data)
        return {'message': gettext('distributorUpdated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.delete('/<int:distributor_id>')
@bp.output(Message)
@jwt_required()
def delete_distributors(distributor_id):
    '''Delete distributors'''

    try:
        distributors.delete_distributor(distributor_id)
        return {'message': gettext('distributorDeleted')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))
