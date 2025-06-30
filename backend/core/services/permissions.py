from sqlalchemy import and_
from core.app import db
from core.models import Group, Module, Permission


def get_permissions_by_group_id(group_id: int, search: str = '', page: int = 1, per_page: int = 15):
    '''Get permissions by group_id'''

    query = Group.id == group_id
    if search:
        query = and_(Group.id == group_id, Module.name.ilike(f'%{search}%'))

    total = db.session.query(Module).count()
    return list(db.session.execute(
        db.session.query(
            *Permission.__table__.c,
            Module.name.label('module_name'))
        .select_from(Permission)
        .join(Module)
        .join(Group)
        .filter(query)
        .order_by(Module.id)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total
