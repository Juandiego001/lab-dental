from core.app import db
from core.models import Brand
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_brands(search: str, page: int, per_page: int):
    '''Get brands'''

    query = Brand.status == 'ACTIVE'
    if search:
        query = and_(Brand.status == 'ACTIVE',
                     or_(Brand.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Brand).filter(query),
                       page=page, per_page=per_page, count=True)


def get_brand_by_id(brand_id: int):
    '''Get brand by brand id'''

    return db.session.query(Brand).filter(Brand.id == brand_id).first()


def check_brand_exists(brand_id: int):
    '''Check if brand exists'''

    return db.session.query(Brand).filter(Brand.id == brand_id).first()


def update_brand(brand_id: int, brand_load):
    '''Update brand'''

    if not check_brand_exists(brand_id):
        raise HTTPException('Brand not found')

    db.session.merge(brand_load)
    db.session.commit()


def delete_brand(brand_id: int):
    '''Delete brand'''

    db.session.merge(Brand(id=brand_id, status='INACTIVE'))
    db.session.commit()
