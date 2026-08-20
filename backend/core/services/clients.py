from core.app import db
from core.models import Client, Distributor, User
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException

from core.services.distributors import get_distributor_from_user


def search_clients(current_user: User, distributor_id: int, client_id: int, name: str, phone: str, page: int, per_page: int, sort_by: dict = None):
    '''Search clients'''

    order_by = Client.id.desc()
    if sort_by:
        if sort_by['key'] == 'name':
            order_by = Client.name
        elif sort_by['key'] == 'phone':
            order_by = Client.phone
        elif sort_by['key'] == 'distributorName':
            order_by = Distributor.name
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Client.status == 'ACTIVE']
    with_client_id = None
    if distributor_id:
        query.append(Client.distributor_id == distributor_id)
    if name:
        query.append(Client.name.ilike(f'%{name}%'))
    if phone:
        query.append(Client.phone.ilike(f'%{phone}%'))

    query_stmt = db.session.query(
        *Client.__table__.c,
        Distributor.name.label('distributor_name'))\
        .join(Distributor)

    if client_id:
        query.append(Client.id != client_id)
        with_client_id = query_stmt\
            .filter(Client.id == client_id)\
            .all()

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(Client.distributor_id == distributor.id)

    total = db.session.query(Client)\
        .filter(*query)\
        .count()
    total += len(with_client_id) if with_client_id else 0
    clients = query_stmt\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_client_id:
        return clients, total
    return with_client_id + clients, total


def get_client_by_id(client_id: int):
    '''Get client by client id'''

    return db.session.query(
        *Client.__table__.c,
        Distributor.name.label('distributor_name'))\
        .join(Distributor)\
        .filter(Client.id == client_id)\
        .first()


def get_client_by_name_and_distributor(distributor_id: int, name: str) -> Client | None:
    '''Get client by name and distributor to verify if existing'''

    return db.session.query(Client).filter(and_(Client.distributor_id == distributor_id, Client.name == name, Client.status == 'ACTIVE')).first()


def create_client(current_user: User, client_model: Client):
    '''Create a client'''

    if not (client_model.distributor_id):
        distributor: Distributor = get_distributor_from_user(current_user)
        client_model.distributor_id = distributor.id

    '''Validates client with existing name'''
    if get_client_by_name_and_distributor(client_model.distributor_id, client_model.name):
        pass


    db.session.add(client_model)
    db.session.commit()


def check_client_exists(client_id: int):
    '''Check if client exists'''

    return db.session.query(Client).filter(Client.id == client_id).first()


def update_client(client_id: int, client_load):
    '''Update client'''

    if not check_client_exists(client_id):
        raise HTTPException('Client not found')

    db.session.merge(client_load)
    db.session.commit()


def delete_client(client_id: int):
    '''Delete client'''

    db.session.merge(Client(id=client_id, status='INACTIVE'))
    db.session.commit()
