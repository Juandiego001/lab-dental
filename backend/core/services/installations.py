from core.app import db
from core.models import Installation
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_installations(search: str, page: int, per_page: int):
    '''Get installations'''

    query = Installation.status == 'ACTIVE'
    if search:
        query = and_(Installation.status == 'ACTIVE',
                     or_(Installation.full_name.ilike(f'%{search}%'),
                         Installation.document.ilike(f'%{search}%'),
                         Installation.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Installation).filter(query),
                       page=page, per_page=per_page)


def get_installation_by_id(installation_id: int):
    '''Get installation by installation id'''

    return db.session.query(Installation).filter(Installation.id == installation_id).first()


def check_installation_exists(installation_id: int):
    '''Check if installation exists'''

    return db.session.query(Installation).filter(Installation.id == installation_id).first()


def update_installation(installation_id: int, installation_load):
    '''Update installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException('Installation not found')

    db.session.merge(installation_load)
    db.session.commit()


def delete_installation(installation_id: int):
    '''Delete installation'''

    db.session.merge(Installation(id=installation_id, status='INACTIVE'))
    db.session.commit()
