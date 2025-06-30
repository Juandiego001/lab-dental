from core.app import db
from core.models import Client, Distributor
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_clients(search: str, page: int, per_page: int):
    '''Get clients'''

    query = Client.status == 'ACTIVE'
    if search:
        query = and_(Client.status == 'ACTIVE',
                     or_(Client.name.ilike(f'%{search}%')))

    total = db.session.query(Client).count()

    return list(db.session.execute(
        db.session.query(
            *Client.__table__.c,
            Distributor.name.label('distributor_name'))
        .join(Distributor)
        .filter(query)
        .order_by(Client.id.desc())
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_client_by_id(client_id: int):
    '''Get client by client id'''

    return db.session.query(
        *Client.__table__.c,
        Distributor.name.label('distributor_name'))\
        .join(Distributor)\
        .filter(Client.id == client_id)\
        .first()


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
