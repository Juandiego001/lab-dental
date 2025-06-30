from core.app import db
from core.services import clients
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.clients import ClientInUpdate, ClientInCreate, ClientOut, ClientsOut


bp = APIBlueprint('clients', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(ClientsOut)
def get_clients(query_data):
    '''Get clients'''

    try:
        results, total = clients.get_clients(query_data['search'],
                                  query_data['page'],
                                  query_data['per_page'])

        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:client_id>')
@bp.output(ClientOut)
def get_client(client_id):
    '''Get client'''

    try:
        return clients.get_client_by_id(client_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ClientInCreate, arg_name='client')
def create_clients(client):
    '''Create clients'''

    try:
        db.session.add(client)
        db.session.commit()
        return {'message': 'Client registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:client_id>')
@bp.input(ClientInUpdate)
@bp.output(Message)
def update_clients(client_id, json_data):
    '''Update client'''
    try:
        clients.update_client(client_id, json_data)
        return {'message': 'Client updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:client_id>')
@bp.output(Message)
def delete_clients(client_id):
    '''Delete clients'''

    try:
        clients.delete_client(client_id)
        return {'message': 'Client deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
