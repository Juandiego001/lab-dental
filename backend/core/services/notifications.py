from core.app import db
from werkzeug.exceptions import HTTPException
from sqlalchemy import Boolean, func, delete, and_
from core.services.distributors import get_distributor_from_user
from core.models import Distributor, Notification, Module, NotificationModule, User, UserNotification


def search_notifications(current_user: User, distributor_id: int, name: str, page: int, per_page: int, sort_by: dict = None) -> tuple[list, int]:
    '''Search notifications'''

    order_by = Notification.id.desc()
    if sort_by:
        if sort_by['key'] == 'name':
            order_by = Notification.name
        elif sort_by['key'] == 'distributorName':
            order_by = Distributor.name
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Notification.status == 'ACTIVE']
    if distributor_id:
        query.append(Notification.distributor_id == distributor_id)
    if name:
        query.append(Notification.name.ilike(f'%{name}%'))

    if current_user.role == 'ADMIN':
        total = db.session.query(Notification).filter(*query).count()
        return list(db.session.execute(
            db.session.query(
                *Notification.__table__.c,
                Distributor.name.label('distributor_name'),
            )
            .select_from(Notification)
            .join(Distributor)
            .filter(*query)
            .order_by(order_by)
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).unique()), total

    distributor: Distributor = get_distributor_from_user(current_user)
    query.append(Distributor.id == distributor.id)
    total = db.session.query(Notification)\
        .join(Distributor)\
        .filter(*query).count()
    return list(db.session.execute(
        db.session.query(
            *Notification.__table__.c
        )
        .select_from(Notification)
        .join(Distributor)
        .filter(*query)
        .order_by(order_by)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_notification_by_id(notification_id: int):
    '''Get notification by notification id'''

    return db.session.query(
        *Notification.__table__.c,
        Distributor.name.label('distributor_name'),
        func.array_agg(User.id).label('users_ids')
    )\
        .select_from(Notification)\
        .outerjoin(UserNotification)\
        .outerjoin(User)\
        .outerjoin(Distributor)\
        .filter(Notification.id == notification_id)\
        .group_by(Notification.id, Notification.name, Distributor.name)\
        .first()


def create_notification(current_user: User, notification_object: Notification, users_ids: list):
    '''Create a notification'''

    # Get distributor_id if current_user not exists
    if (not notification_object.distributor_id):
        notification_object.distributor_id = get_distributor_from_user(
            current_user).id

    # Creation of notification
    db.session.add(notification_object)
    db.session.flush()

    # Creation of user_notifications
    user_notifications = [UserNotification(notification_id=notification_object.id, user_id=user_id)
                          for user_id in users_ids]
    db.session.add_all(user_notifications)

    # Creation of permissions
    modules = db.session.query(Module).all()
    notification_modules = [
        NotificationModule(
            notification_id=notification_object.id,
            module_id=module.id,
            create=False,
            update=False,
            delete=False
        )
        for module in modules
    ]
    db.session.add_all(notification_modules)

    db.session.commit()


def check_notification_exists(notification_id: int):
    '''Check if notification exists'''

    return db.session.query(Notification).filter(Notification.id == notification_id).first()


def update_notification(notification_id: int, json_data: tuple[Notification, list]):
    '''Update notification'''

    notification_obj, users_ids = json_data

    if not check_notification_exists(notification_id):
        raise HTTPException('Notification not found')

    # Delete users from notification
    db.session.execute(delete(UserNotification).where(
        UserNotification.notification_id == notification_id))

    # Insert users in notification again
    user_notifications = [UserNotification(notification_id=notification_id, user_id=user_id)
                          for user_id in users_ids]
    db.session.add_all(user_notifications)

    db.session.merge(notification_obj)
    db.session.commit()


def delete_notification(notification_id: int):
    '''Delete notification'''

    db.session.merge(Notification(id=notification_id, status='INACTIVE'))
    db.session.commit()


def get_notifications_modules_by_notification_id(current_user: User, notification_id: int, search: str = '', page: int = 1, per_page: int = 15):
    '''Get notifications modules by notification id'''

    query = and_(
        Notification.id == notification_id,
        Module.name.in_(
            ['installations', 'warranties'])
    )

    # Distributors users should not have access to some modules
    # if current_user.role != 'ADMIN':
    #     module_filter = Module.name.not_in(
    #         ['distributors', 'lists', 'reasons'])
    #     query = and_(query, module_filter)

    total = db.session.query(Module).filter(query).count()
    return list(db.session.execute(
        db.session.query(
            *NotificationModule.__table__.c,
            Module.name.label('module_name'))
        .select_from(NotificationModule)
        .join(Module, NotificationModule.module_id == Module.id)
        .join(Notification, NotificationModule.notification_id == Notification.id)
        .filter(query)
        .order_by(Module.name)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def update_notifications_modules(data: dict):
    '''Update notifications modules'''

    if not 'id' in data or not data['id']:
        raise Exception('Permission ID not found')

    notification_module_id = data['id']
    _, distributor_id, module_name = db.session.query(
        Notification.id, Distributor.id, Module.name)\
        .select_from(NotificationModule)\
        .join(Module, NotificationModule.module_id == Module.id)\
        .join(Notification, NotificationModule.notification_id == Notification.id)\
        .join(Distributor, Notification.distributor_id == Distributor.id)\
        .filter(NotificationModule.id == notification_module_id)\
        .first()

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
            (create or update or delete):
        raise Exception('Forbiden permission assignment')

    if distributor_id != 1 and\
        module_name in modules_ban and\
            (create or update or delete):
        raise Exception('Forbiden permission assignment')

    new_notification_module = NotificationModule(
        id=notification_module_id,
        create=create,
        update=update,
        delete=delete
    )

    db.session.merge(new_notification_module)
    db.session.commit()
