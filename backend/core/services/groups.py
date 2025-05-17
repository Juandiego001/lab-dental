from core.app import db
from core.models import Group
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_groups(search: str, page: int, per_page: int):
    '''Get groups'''

    query = Group.status == 'ACTIVE'
    if search:
        query = and_(Group.status == 'ACTIVE',
                     or_(Group.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Group).filter(query),
                       page=page, per_page=per_page)


def get_group_by_id(group_id: int):
    '''Get group by group id'''

    return db.session.query(Group).filter(Group.id == group_id).first()


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
