from core.app import db
from core.models import Reason
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_reasons(search: str, page: int, per_page: int):
    '''Get reasons'''

    query = Reason.status == 'ACTIVE'
    if search:
        query = and_(Reason.status == 'ACTIVE',
                     or_(Reason.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Reason).filter(query),
                       page=page, per_page=per_page, count=True)


def get_reason_by_id(reason_id: int):
    '''Get reason by reason id'''

    return db.session.query(Reason).filter(Reason.id == reason_id).first()


def check_reason_exists(reason_id: int):
    '''Check if reason exists'''

    return db.session.query(Reason).filter(Reason.id == reason_id).first()


def update_reason(reason_id: int, reason_load):
    '''Update reason'''

    if not check_reason_exists(reason_id):
        raise HTTPException('Reason not found')

    db.session.merge(reason_load)
    db.session.commit()


def delete_reason(reason_id: int):
    '''Delete reason'''

    db.session.merge(Reason(id=reason_id, status='INACTIVE'))
    db.session.commit()
