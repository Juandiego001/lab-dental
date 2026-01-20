from core.app import db
from core.models import Manual
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_manuals(search: str, page: int, per_page: int):
    '''Get manuals'''

    query = Manual.status == 'ACTIVE'
    # if search:
    #     query = and_(Manual.status == 'ACTIVE',
    #                  or_(Manual.id.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Manual).filter(query),
                       page=page, per_page=per_page, count=True)


def get_manual_by_id(manual_id: int):
    '''Get manual by manual id'''

    return db.session.query(Manual).filter(Manual.id == manual_id).first()


def check_manual_exists(manual_id: int):
    '''Check if manual exists'''

    return db.session.query(Manual).filter(Manual.id == manual_id).first()


def update_manual(manual_id: int, manual_load):
    '''Update manual'''

    if not check_manual_exists(manual_id):
        raise HTTPException('Manual not found')

    db.session.merge(manual_load)
    db.session.commit()


def delete_manual(manual_id: int):
    '''Delete manual'''

    db.session.merge(Manual(id=manual_id, status='INACTIVE'))
    db.session.commit()
