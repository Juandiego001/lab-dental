from core.app import db
from core.models import Brand, Category, Equipment
from sqlalchemy import or_, and_, literal, func
from werkzeug.exceptions import HTTPException


def get_equipments(search: str, page: int, per_page: int):
    '''Get equipments'''

    query = Equipment.status == 'ACTIVE'
    if search:
        query = and_(Equipment.status == 'ACTIVE',
                     or_(
                         Equipment.serial.ilike(f'%{search}%'),
                         Equipment.model.ilike(f'%{search}%'),
                         literal(search).ilike('%' + Equipment.serial + '%'),
                         literal(search).ilike('%' + Equipment.model + '%')))

    total = db.session.query(Equipment).filter(query).count()

    return list(db.session.execute(
        db.session.query(
            *Equipment.__table__.c,
            func.concat(Equipment.model, ' - ', Equipment.serial).label('serial_model'),
            Brand.name.label('brand_name'),
            Category.name.label('category_name')
        )
        .join(Brand)
        .join(Category)
        .filter(query)
        .order_by(Equipment.id.desc())
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_equipment_by_id(equipment_id: int):
    '''Get equipment by equipment id'''

    return db.session.query(
        *Equipment.__table__.c,
        Brand.name.label('brand_name'),
        Category.name.label('category_name'))\
        .join(Brand)\
        .join(Category)\
        .filter(Equipment.id == equipment_id)\
        .first()


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
