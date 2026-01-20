from core.app import db
from core.models import Part
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_parts(search: str, page: int, per_page: int):
    '''Get parts'''

    query = Part.status == 'ACTIVE'
    if search:
        query = and_(Part.status == 'ACTIVE',
                     or_(Part.serial.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Part).filter(query),
                       page=page, per_page=per_page, count=True)


def get_part_by_id(part_id: int):
    '''Get part by part id'''

    return db.session.query(Part).filter(Part.id == part_id).first()


def check_part_exists(part_id: int):
    '''Check if part exists'''

    return db.session.query(Part).filter(Part.id == part_id).first()


def update_part(part_id: int, part_load):
    '''Update part'''

    if not check_part_exists(part_id):
        raise HTTPException('Part not found')

    db.session.merge(part_load)
    db.session.commit()


def delete_part(part_id: int):
    '''Delete part'''

    db.session.merge(Part(id=part_id, status='INACTIVE'))
    db.session.commit()
