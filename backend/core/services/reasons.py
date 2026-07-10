from core.app import db
from core.models import Reason
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def search_reasons(category_id: int, name: str, slug: str, description: str, page: int, per_page: int, sort_by: dict = None):
    '''Search reasons'''

    order_by = Reason.id.desc()
    if sort_by:
        if sort_by['key'] == 'name':
            order_by = Reason.name
        elif sort_by['key'] == 'slug':
            order_by = Reason.slug
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Reason.status == 'ACTIVE']
    if category_id:
        query.append(Reason.category_id == category_id)
    if name:
        query.append(Reason.name.ilike(f'%{name}%'))
    if slug:
        query.append(Reason.slug.ilike(f'%{slug}%'))
    if description:
        query.append(Reason.description.ilike(f'%{description}%'))

    total = db.session.query(Reason)\
        .filter(*query)\
        .count()

    reasons = db.session.query(Reason)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()
    return reasons, total


def get_reason_by_id(reason_id: int):
    '''Get reason by reason id'''

    return db.session.query(Reason).filter(Reason.id == reason_id).first()


def check_reason_exists(reason_id: int):
    '''Check if reason exists'''

    return db.session.query(Reason).filter(Reason.id == reason_id).first()


def update_reason(reason_id: int, reason_load: dict):
    '''Update reason'''

    if not check_reason_exists(reason_id):
        raise HTTPException('Reason not found')

    db.session.merge(Reason(**reason_load))
    db.session.commit()


def delete_reason(reason_id: int):
    '''Delete reason'''

    db.session.merge(Reason(id=reason_id, status='INACTIVE'))
    db.session.commit()
