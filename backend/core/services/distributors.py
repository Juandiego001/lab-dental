import re
import unicodedata
from core.app import db
from core.models import Client, Distributor, DistributorList, List_, User, UserList
from sqlalchemy import func, and_, select
from werkzeug.exceptions import HTTPException


def search_distributors(current_user: User, distributors_ids: list[int], name: str, page: int, per_page: int):
    '''Search distributors'''

    query = [Distributor.status == 'ACTIVE']
    with_distributors_ids = None
    if name:
        query.append(Distributor.name.ilike(f'%{name}%'))
    if distributors_ids:
        query.append(Distributor.id.not_in(distributors_ids))
        with_distributors_ids = db.session.query(Distributor)\
            .filter(Distributor.id.in_(distributors_ids))\
            .all()

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(Distributor.id == distributor.id)

    total = db.session.query(Distributor)\
        .filter(*query).count()
    total += len(with_distributors_ids) if with_distributors_ids else 0

    distributors = db.session.query(Distributor)\
        .filter(*query)\
        .order_by(Distributor.id.desc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_distributors_ids:
        return distributors, total
    return with_distributors_ids + distributors, total


def get_clients_by_distributor_id(distributor_id: int, search: str):
    '''Get clients by distributor id'''

    query = [and_(Distributor.id == distributor_id, Client.status == 'ACTIVE')]
    if search:
        query.append(Client.name.ilike(f'%{search}%'))

    return db.paginate(db.session.query(Client)
                       .join(Distributor)
                       .filter(*query),
                       page=1, per_page=15)


def get_distributor_from_user(user: User) -> Distributor:
    '''Get distributor from user'''

    return db.session.query(Distributor)\
        .select_from(Distributor)\
        .join(DistributorList)\
        .join(List_)\
        .join(UserList)\
        .join(User)\
        .filter(and_(User.id == user.id, List_.is_main))\
        .first()


def get_distributor_by_id(distributor_id: int):
    '''Get distributor by distributor id'''

    return db.session.query(Distributor).filter(Distributor.id == distributor_id).first()


def check_distributor_exists(distributor_id: int):
    '''Check if distributor exists'''

    return db.session.query(Distributor).filter(Distributor.id == distributor_id).first()


def create_distributor(distributor: Distributor):
    '''Create distributor'''

    distributor_name = distributor.name
    db.session.add(distributor)

    # Slug generation process
    slug = f'Main {distributor_name}'.lower()
    slug = unicodedata.normalize('NFKD', slug).encode(
        'ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')

    list_ = List_(name=f'Main {distributor_name}', slug=slug, is_main=True)
    db.session.add(list_)
    db.session.flush()

    distributor_list = DistributorList(
        distributor_id=distributor.id, list_id=list_.id)
    db.session.add(distributor_list)
    db.session.commit()


def update_distributor(distributor_id: int, distributor_load):
    '''Update distributor'''

    if not check_distributor_exists(distributor_id):
        raise HTTPException('Distributor not found')

    db.session.merge(distributor_load)
    db.session.commit()


def delete_distributor(distributor_id: int):
    '''Delete distributor'''

    distributor_list_subquery = db.session.query(DistributorList.list_id).filter(
        DistributorList.distributor_id == distributor_id).subquery()

    lists_ = db.session.query(
        List_.id.label('list_id'),
        func.array_agg(DistributorList.distributor_id).label('distributors')
    )\
        .select_from(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(Distributor.status == 'ACTIVE', List_.id.in_(select(distributor_list_subquery)))\
        .group_by(List_.id)\
        .all()

    unique_lists = [each_list.list_id for each_list in lists_ if len(
        each_list.distributors) == 1]
    for list_id in unique_lists:
        db.session.merge(List_(id=list_id, status='INACTIVE'))

    db.session.merge(Distributor(id=distributor_id, status='INACTIVE'))
    db.session.commit()
