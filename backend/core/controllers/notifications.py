from core.services import notifications
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from flask_jwt_extended import jwt_required, current_user
from core.schemas.notifications import NotificationInUpdate, NotificationInCreate, NotificationModuleIn, NotificationOut, NotificationSearch, NotificationsOut, NotificationsModulesOut
from flask_babel import gettext


bp = APIBlueprint('notifications', __name__)


@bp.post('/search')
@bp.input(NotificationSearch)
@bp.output(NotificationsOut)
@jwt_required()
def search_notifications(json_data):
    '''Search notifications'''

    try:
        results, total = notifications.search_notifications(
            current_user=current_user,
            distributor_id=json_data['distributor_id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:notification_id>')
@bp.output(NotificationOut)
@jwt_required()
def get_notification(notification_id):
    '''Get notification'''

    try:
        return notifications.get_notification_by_id(notification_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(NotificationInCreate)
@bp.output(Message)
@jwt_required()
def create_notifications(json_data):
    '''Create notifications'''

    try:
        notification_object, users_ids = json_data
        notifications.create_notification(
            current_user, notification_object, users_ids)
        return {'message': gettext('notificationCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:notification_id>')
@bp.input(NotificationInUpdate)
@bp.output(Message)
@jwt_required()
def update_notifications(notification_id, json_data):
    '''Update notification'''

    try:
        notifications.update_notification(notification_id, json_data)
        return {'message': gettext('notificationUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:notification_id>')
@bp.output(Message)
@jwt_required()
def delete_notifications(notification_id):
    '''Delete notifications'''

    try:
        notifications.delete_notification(notification_id)
        return {'message': gettext('notificationDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/modules/<int:notification_id>')
@bp.input(Pagination, location='query')
@bp.output(NotificationsModulesOut)
@jwt_required()
def get_notifications_modules_by_notification_id(notification_id: int, query_data):
    '''Get notifications modules by notification id'''

    try:
        results, total = notifications.get_notifications_modules_by_notification_id(
            current_user,
            notification_id,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/modules')
@bp.input(NotificationModuleIn)
@jwt_required()
def update_permissions(json_data):
    '''Update permissions'''

    try:
        notifications.update_notifications_modules(json_data)
        return {'message': gettext('notificationsModulesUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))
