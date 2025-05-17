from core.app import db
from core.models import Warranty
from sqlalchemy import or_, and_
from bcrypt import checkpw
from werkzeug.exceptions import HTTPException


def get_warranties(search: str, page: int, per_page: int):
    '''Get warranties'''

    query = Warranty.status == 'ACTIVE'
    if search:
        query = and_(Warranty.status == 'ACTIVE',
                     or_(Warranty.full_name.ilike(f'%{search}%'),
                         Warranty.document.ilike(f'%{search}%'),
                         Warranty.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Warranty).filter(query),
                       page=page, per_page=per_page)


def get_warranty_by_id(warranty_id: int):
    '''Get warranty by warranty id'''

    return db.session.query(Warranty).filter(Warranty.id == warranty_id).first()


def check_warranty_exists(warranty_id: int):
    '''Check if warranty exists'''

    return db.session.query(Warranty).filter(Warranty.id == warranty_id).first()


def update_warranty(warranty_id: int, warranty_load):
    '''Update warranty'''

    if not check_warranty_exists(warranty_id):
        raise HTTPException('Warranty not found')

    db.session.merge(warranty_load)
    db.session.commit()


def delete_warranty(warranty_id: int):
    '''Delete warranty'''

    db.session.merge(Warranty(id=warranty_id, status='INACTIVE'))
    db.session.commit()
