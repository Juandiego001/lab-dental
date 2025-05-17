from core.app import db
from core.models import Distributor
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_distributors(search: str, page: int, per_page: int):
    '''Get distributors'''

    query = Distributor.status == 'ACTIVE'
    if search:
        query = and_(Distributor.status == 'ACTIVE',
                     or_(Distributor.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Distributor).filter(query),
                       page=page, per_page=per_page)


def get_distributor_by_id(distributor_id: int):
    '''Get distributor by distributor id'''

    return db.session.query(Distributor).filter(Distributor.id == distributor_id).first()


def check_distributor_exists(distributor_id: int):
    '''Check if distributor exists'''

    return db.session.query(Distributor).filter(Distributor.id == distributor_id).first()


def update_distributor(distributor_id: int, distributor_load):
    '''Update distributor'''

    if not check_distributor_exists(distributor_id):
        raise HTTPException('Distributor not found')

    db.session.merge(distributor_load)
    db.session.commit()


def delete_distributor(distributor_id: int):
    '''Delete distributor'''

    db.session.merge(Distributor(id=distributor_id, status='INACTIVE'))
    db.session.commit()
