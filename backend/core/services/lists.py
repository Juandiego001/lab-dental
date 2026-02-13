import re
import unicodedata
from core.app import db
from sqlalchemy import case, or_, and_, func, delete
from werkzeug.exceptions import HTTPException
from core.models import Distributor, List_, DistributorList, User, UserList


def get_lists(search: str, page: int, per_page: int):
    '''Get lists'''

    query = List_.status == 'ACTIVE'
    if search:
        query = and_(query, List_.name.ilike(f'%{search}%'))

    return db.paginate(db.session.query(List_).filter(query, List_.is_main == False).order_by(List_.id.desc()),
                       page=page, per_page=per_page, count=True)


def get_list_by_id(list_id: int):
    '''Get list by lists id'''

    return db.session.query(
        *List_.__table__.c,
        func.array_agg(case((Distributor.status == 'ACTIVE',
                       Distributor.id), else_=None)).label('distributors_ids'),
        func.array_agg(case((User.status == 'ACTIVE', User.id), else_=None)).label('users_ids'))\
        .select_from(List_)\
        .outerjoin(DistributorList)\
        .outerjoin(Distributor, DistributorList .distributor_id == Distributor.id)\
        .outerjoin(UserList)\
        .outerjoin(User, UserList.user_id == User.id)\
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


def get_users_and_existing(search: str, users_ids: list[int] = []):
    '''Get users of a list for autocomplete. Existing users and new ones'''

    query = [User.status == 'ACTIVE']

    if search:
        query.append(User.full_name.ilike(f'%{search}%'))

    return db.paginate(db.session.query(User)
                       .filter(or_(and_(*query), User.id.in_(users_ids))),
                       page=1, per_page=15)


def get_distributors_and_existing(search: str, distributors_ids: list[int] = []):
    '''Get distributors of a list for autocomplete. Existing distributors and new ones'''

    query = [Distributor.status == 'ACTIVE']

    if search:
        query.append(Distributor.name.ilike(f'%{search}%'))

    return db.paginate(db.session.query(Distributor)
                       .filter(or_(and_(*query), Distributor.id.in_(distributors_ids))),
                       page=1, per_page=15)


def update_list(list_id: int, list_data: dict):
    '''Update list'''

    if not check_list_exists(list_id):
        raise HTTPException('List not found')

    # Delete old distributors ids
    db.session.execute(delete(DistributorList).where(
        DistributorList.list_id == list_id))

    # Delete old users ids
    db.session.execute(delete(UserList).where(UserList.list_id == list_id))

    # Creation of distributors_ids and users_ids
    if 'distributors_ids' in list_data and len(list_data['distributors_ids']):
        distributors_ids = list_data.pop('distributors_ids')
        distributors_ids = [DistributorList(
            distributor_id=distributor_id, list_id=list_id) for distributor_id in distributors_ids]
        db.session.add_all(distributors_ids)

    if 'users_ids' in list_data and len(list_data['users_ids']):
        users_ids = list_data.pop('users_ids')
        users_ids = [UserList(user_id=user_id, list_id=list_id)
                     for user_id in users_ids]
        db.session.add_all(users_ids)

    db.session.merge(List_(**list_data))
    db.session.commit()


def delete_list(list_id: int):
    '''Delete list'''

    db.session.merge(List_(id=list_id, status='INACTIVE'))
    db.session.commit()
