from core.app import db
from core.models import Brand, Distributor, DistributorBrand, User
from werkzeug.exceptions import HTTPException

from core.services.distributors import get_distributor_from_user


def search_brands(current_user: User, brands_ids: list[int], name: str, slug: str, page: int, per_page: int, sort_by: dict = None):
    '''Search brands'''

    order_by = Brand.id.desc()
    if sort_by and isinstance(sort_by, dict):
        sort_key = sort_by.get('key')
        sort_order = sort_by.get('order', 'asc')
        if sort_key and hasattr(Brand, sort_key):
            column = getattr(Brand, sort_key)
            if sort_order == 'desc':
                order_by = column.desc()
            else:
                order_by = column.asc()

    query = [Brand.status == 'ACTIVE']
    with_brand_id = None
    if name:
        query.append(Brand.name.ilike(f'%{name}%'))
    if slug:
        query.append(Brand.slug.ilike(f'%{slug}%'))

    if brands_ids:
        query.append(Brand.id.not_in(brands_ids))
        with_brand_id = db.session.query(Brand)\
            .filter(Brand.id.in_(brands_ids))\
            .all()

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        brands_ids = db.session.scalars(db.session.query(DistributorBrand.brand_id).filter(
            DistributorBrand.distributor_id == distributor.id)).all()
        query.append(Brand.id.in_(brands_ids))

    total = db.session.query(Brand)\
        .filter(*query)\
        .count()
    total += len(with_brand_id) if with_brand_id else 0

    brands = db.session.query(Brand)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_brand_id:
        return brands, total
    return with_brand_id + brands, total


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
