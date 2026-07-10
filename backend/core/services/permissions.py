from core.app import db
from sqlalchemy import and_
from core.models import Distributor, Group, Module, Permission, User


def get_permissions_by_group_id(current_user: User, group_id: int, search: str = '', page: int = 1, per_page: int = 15):
    '''Get permissions by group_id'''

    query = and_(
        Group.id == group_id,
        Module.name.not_in(
            ['manuals', 'forums', 'parts', 'strapi'])
    )

    # Distributors users should not have access to some modules
    if current_user.role != 'ADMIN':
        module_filter = Module.name.not_in(
            ['distributors', 'lists'])
        query = and_(query, module_filter)

    total = db.session.query(Module).filter(query).count()
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


def update_permissions(data: dict):
    '''Update permissions'''

    if not 'id' in data or not data['id']:
        raise Exception('Permission ID not found')

    permission_id = data['id']
    group_id, distributor_id, module_name = db.session.query(
        Group.id, Distributor.id, Module.name
    ).select_from(
        Permission
    ).join(Module,
           Permission.module_id == Module.id
           ).join(Group,
                  Permission.group_id == Group.id
                  ).join(Distributor,
                         Group.distributor_id == Distributor.id
                         ).filter(
        Permission.id == permission_id
    ).first()

    read = data['read']
    create = data['create']
    update = data['update']
    delete = data['delete']

    modules_only_read = ['brands', 'categories', 'equipments']
    modules_ban = ['distributors', 'lists']

    if distributor_id != 1 and\
        module_name in modules_only_read and\
            (create or update or delete):
        raise Exception('Forbiden permission assignment')

    if distributor_id != 1 and\
        module_name in modules_ban and\
            (read or create or update or delete):
        raise Exception('Forbiden permission assignment')

    if distributor_id != 1 and\
        module_name in modules_ban and\
            (read or create or update or delete):
        raise Exception('Forbiden permission assignment')

    if group_id == 1:
        raise Exception('Forbiden permission update')

    new_permission = Permission(
        id=permission_id,
        create=create,
        read=read,
        update=update,
        delete=delete
    )

    db.session.merge(new_permission)
    db.session.commit()
