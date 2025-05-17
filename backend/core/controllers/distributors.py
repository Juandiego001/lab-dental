from core.app import db
from core.services import distributors
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.distributors import DistributorInUpdate, DistributorInCreate, DistributorOut, DistributorsOut


bp = APIBlueprint('distributors', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(DistributorsOut)
def get_distributors(query_data):
    '''Get distributors'''

    try:
        return {'items': distributors.get_distributors(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:distributor_id>')
@bp.output(DistributorOut)
def get_distributor(distributor_id):
    '''Get distributor'''

    try:
        return distributors.get_distributor_by_id(distributor_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(DistributorInCreate, arg_name='distributor')
def create_distributors(distributor):
    '''Create distributors'''

    try:
        db.session.add(distributor)
        db.session.commit()
        return {'message': 'Distributor registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:distributor_id>')
@bp.input(DistributorInUpdate)
@bp.output(Message)
def update_distributors(distributor_id, json_data):
    '''Update distributor'''
    try:
        distributors.update_distributor(distributor_id, json_data)
        return {'message': 'Distributor updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:distributor_id>')
@bp.output(Message)
def delete_distributors(distributor_id):
    '''Delete distributors'''

    try:
        distributors.delete_distributor(distributor_id)
        return {'message': 'Distributor deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
