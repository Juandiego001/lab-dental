from core.app import db
from core.models import Distributor, Group, Module, Permission, User, UserGroup
from sqlalchemy import func, or_, and_
from werkzeug.exceptions import HTTPException

from core.services.distributors import get_distributor_id_from_user


def get_groups(current_user: User, search: str, page: int, per_page: int) -> tuple[list, int]:
    '''Get groups'''

    query = Group.status == 'ACTIVE'
    if search:
        query = and_(Group.status == 'ACTIVE',
                     or_(Group.name.ilike(f'%{search}%')))

    if current_user.role == 'ADMIN':
        total = db.session.query(Group).filter(query).count()
        return list(db.session.execute(
            db.session.query(
                *Group.__table__.c,
                Distributor.name.label('distributor_name'),
            )
            .select_from(Group)
            .join(Distributor)
            .filter(query)
            .order_by(Group.id.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).unique()), total

    distributor_id = get_distributor_id_from_user(current_user.id)
    query = and_(query, Distributor.id == distributor_id)
    total = db.session.query(Group).filter(query).count()
    return list(db.session.execute(
        db.session.query(Group)
        .select_from(Group)
        .join(Distributor)
        .filter(query)
        .order_by(Group.id.desc())
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_group_by_id(group_id: int):
    '''Get group by group id'''

    return db.session.query(
        *Group.__table__.c,
        func.array_agg(User.id).label('users_ids')
    )\
        .select_from(Group)\
        .join(UserGroup)\
        .join(User)\
        .filter(Group.id == group_id)\
        .group_by(Group.id, Group.name)\
        .first()


def create_group(current_user: User, group_object: Group, users_ids: list):
    '''Create a group'''

    # Get distributor_id if current_user not exists
    group_object.distributor_id = group_object.distributor_id if group_object.distributor_id else get_distributor_id_from_user(
        current_user.id)

    # Creation of group
    db.session.add(group_object)
    db.session.flush()

    # Creation of user_groups
    user_groups = [UserGroup(group_id=group_object.id, user_id=user_id)
                   for user_id in users_ids]
    db.session.add_all(user_groups)

    # Creation of permissions
    modules = db.session.query(Module).all()
    permissions = [
        Permission(
            group_id=group_object.id,
            module_id=module.id,
            read=False,
            create=False,
            update=False,
            delete=False
        )
        for module in modules
    ]
    db.session.add_all(permissions)

    db.session.commit()


def check_group_exists(group_id: int):
    '''Check if group exists'''

    return db.session.query(Group).filter(Group.id == group_id).first()


def update_group(group_id: int, group_load):
    '''Update group'''

    if not check_group_exists(group_id):
        raise HTTPException('Group not found')

    db.session.merge(group_load)
    db.session.commit()


def delete_group(group_id: int):
    '''Delete group'''

    db.session.merge(Group(id=group_id, status='INACTIVE'))
    db.session.commit()
