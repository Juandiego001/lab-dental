from core.app import db
from core.models import Client, Distributor, User
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException

from core.services.distributors import get_distributor_from_user


def get_clients(current_user: User, search: str, page: int, per_page: int):
    '''Get clients'''

    query = Client.status == 'ACTIVE'
    if search:
        query = and_(Client.status == 'ACTIVE',
                     or_(Client.name.ilike(f'%{search}%')))


    if current_user.role == 'ADMIN':
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
    
    distributor: Distributor = get_distributor_from_user(current_user)
    total = db.session.query(Client).join(Distributor).filter(Distributor.id == distributor.id).count()
    return list(db.session.execute(
        db.session.query(
            *Client.__table__.c,
            Distributor.name.label('distributor_name'))
        .join(Distributor)
        .filter(and_(query, Distributor.id == distributor.id))
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


def create_client(current_user: User, client_model: Client):
    '''Create a client'''

    if not(client_model.distributor_id):
        distributor: Distributor = get_distributor_from_user(current_user)
        client_model.distributor_id = distributor.id
    
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
