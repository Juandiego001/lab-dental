from core.app import db
from sqlalchemy import and_
from core.models import Group, Module, Permission, User


def get_permissions_by_group_id(current_user: User, group_id: int, search: str = '', page: int = 1, per_page: int = 15):
    '''Get permissions by group_id'''

    query = Group.id == group_id

    # Distributors users should not have access to some modules
    if current_user.role != 'ADMIN':
        module_filter = Module.name.not_in(['reasons', 'brands', 'distributors', 'categories', 'strapi', 'lists'])
        query = and_(query, module_filter)
        total = db.session.query(Module).filter(module_filter).count() 
    else:
        total = db.session.query(Module).count() 
        

    return list(db.session.execute(
        db.session.query(
            *Permission.__table__.c,
            Module.name.label('module_name'))
        .select_from(Permission)
        .join(Module)
        .join(Group)
        .filter(query)
        .order_by(Module.name)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def update_permissions_by_group_id(group_id: int):
    '''Update permissions by group_id'''

    pass
