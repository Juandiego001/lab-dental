from core.app import db
from core.models import Equipment
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_equipments(search: str, page: int, per_page: int):
    '''Get equipments'''

    query = Equipment.status == 'ACTIVE'
    if search:
        query = and_(Equipment.status == 'ACTIVE',
                     or_(Equipment.serial.ilike(f'%{search}%'),
                         Equipment.model.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Equipment).filter(query),
                       page=page, per_page=per_page)


def get_equipment_by_id(equipment_id: int):
    '''Get equipment by equipment id'''

    return db.session.query(Equipment).filter(Equipment.id == equipment_id).first()


def check_equipment_exists(equipment_id: int):
    '''Check if equipment exists'''

    return db.session.query(Equipment).filter(Equipment.id == equipment_id).first()


def update_equipment(equipment_id: int, equipment_load):
    '''Update equipment'''

    if not check_equipment_exists(equipment_id):
        raise HTTPException('Equipment not found')

    db.session.merge(equipment_load)
    db.session.commit()


def delete_equipment(equipment_id: int):
    '''Delete equipment'''

    db.session.merge(Equipment(id=equipment_id, status='INACTIVE'))
    db.session.commit()
