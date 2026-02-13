from flask_jwt_extended import jwt_required, current_user
from core.app import db
from core.services import clients
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.clients import ClientInUpdate, ClientInCreate, ClientOut, ClientSearch, ClientsOut


bp = APIBlueprint('clients', __name__)


@bp.post('/search')
@bp.input(ClientSearch)
@bp.output(ClientsOut)
@jwt_required()
def search_clients(json_data):
    '''Search clients'''

    try:
        results, total = clients.search_clients(
            current_user=current_user,
            distributor_id=json_data['distributor_id'],
            client_id=json_data['client_id'],
            name=json_data['name'],
            phone=json_data['phone'],
            page=json_data['page'],
            per_page=json_data['per_page'])

        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:client_id>')
@bp.output(ClientOut)
@jwt_required()
def get_client(client_id):
    '''Get client'''

    try:
        return clients.get_client_by_id(client_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(ClientInCreate, arg_name='client')
@jwt_required()
def create_clients(client):
    '''Create clients'''

    try:
        clients.create_client(current_user, client)
        return {'message': 'Client registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:client_id>')
@bp.input(ClientInUpdate)
@bp.output(Message)
@jwt_required()
def update_clients(client_id, json_data):
    '''Update client'''
    try:
        clients.update_client(client_id, json_data)
        return {'message': 'Client updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:client_id>')
@bp.output(Message)
@jwt_required()
def delete_clients(client_id):
    '''Delete clients'''

    try:
        clients.delete_client(client_id)
        return {'message': 'Client deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
