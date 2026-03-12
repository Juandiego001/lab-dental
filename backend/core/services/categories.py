from core.app import db
from core.models import Category
from werkzeug.exceptions import HTTPException


def search_categories(category_id: int, name: str, slug: str, page: int, per_page: int, sort_by: dict = None):
    '''Search categories'''

    order_by = Category.id.desc()
    if sort_by:
        if sort_by['key'] == 'name':
            order_by = Category.name
        elif sort_by['key'] == 'slug':
            order_by = Category.slug
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Category.status == 'ACTIVE']
    with_category_id = None
    if name:
        query.append(Category.name.ilike(f'%{name}%'))
    if slug:
        query.append(Category.slug.ilike(f'%{slug}%'))
    if category_id:
        query.append(Category.id != category_id)
        with_category_id = db.session.query(Category)\
            .filter(Category.id == category_id)\
            .all()

    total = db.session.query(Category)\
        .filter(*query)\
        .count()
    total += len(with_category_id) if with_category_id else 0

    categories = db.session.query(Category)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_category_id:
        return categories, total
    return with_category_id + categories, total


def get_category_by_id(category_id: int):
    '''Get category by category id'''

    return db.session.query(Category).filter(Category.id == category_id).first()


def check_category_exists(category_id: int):
    '''Check if category exists'''

    return db.session.query(Category).filter(Category.id == category_id).first()


def update_category(category_id: int, category_load):
    '''Update category'''

    if not check_category_exists(category_id):
        raise HTTPException('Category not found')

    db.session.merge(category_load)
    db.session.commit()


def delete_category(category_id: int):
    '''Delete category'''

    db.session.merge(Category(id=category_id, status='INACTIVE'))
    db.session.commit()
