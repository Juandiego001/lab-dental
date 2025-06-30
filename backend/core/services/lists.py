import re
import unicodedata
from core.app import db
from sqlalchemy import or_, and_, func
from werkzeug.exceptions import HTTPException
from core.models import List_, DistributorList, UserList


def get_lists(search: str, page: int, per_page: int):
    '''Get lists'''

    query = List_.status == 'ACTIVE'
    if search:
        query = and_(List_.status == 'ACTIVE',
                     or_(List_.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(List_).filter(query).order_by(List_.id.desc()),
                       page=page, per_page=per_page, count=True)


def get_list_by_id(list_id: int):
    '''Get list by lists id'''

    return db.session.query(
        List_.id, List_.name, func.array_agg(
            DistributorList.distributor_id).label('distributors_ids'),
        func.array_agg(UserList.user_id).label('users_ids'))\
        .select_from(List_)\
        .join(DistributorList)\
        .join(UserList)\
        .filter(List_.id == list_id)\
        .group_by(List_.id, List_.name)\
        .first()


def create_list(list_dict: dict):
    '''Create a list'''

    distributors_ids = list_dict.pop('distributors_ids')
    users_ids = list_dict.pop('users_ids')
    name: str = list_dict['name']

    # Slug generation process
    slug = name.lower()
    slug = unicodedata.normalize('NFKD', slug).encode(
        'ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')

    # Creation of list_
    list_: List_ = List_(name=name, slug=slug)
    db.session.add(list_)
    db.session.flush()

    # Creation of distributors_ids and users_ids
    distributors_ids = [DistributorList(
        distributor_id=distributor_id, list_id=list_.id) for distributor_id in distributors_ids]
    users_ids = [UserList(user_id=user_id, list_id=list_.id)
                 for user_id in users_ids]

    db.session.add_all(distributors_ids)
    db.session.add_all(users_ids)
    db.session.commit()


def check_list_exists(list_id: int):
    '''Check if list exists'''

    return db.session.query(List_).filter(List_.id == list_id).first()


def update_list(list_id: int, lists_load):
    '''Update list'''

    if not check_list_exists(list_id):
        raise HTTPException('List not found')

    db.session.merge(lists_load)
    db.session.commit()


def delete_list(list_id: int):
    '''Delete list'''

    db.session.merge(List_(id=list_id, status='INACTIVE'))
    db.session.commit()
