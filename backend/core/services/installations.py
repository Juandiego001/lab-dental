import uuid
from sqlalchemy.orm import aliased
from sqlalchemy import JSON, and_, func
from datetime import datetime, timedelta
from werkzeug.exceptions import HTTPException
from flask_babel import force_locale, gettext
from core.app import db, FRONTEND_APP_BASE_URL
from core.utils import process_file, send_mail
from werkzeug.datastructures import FileStorage
from sqlalchemy.dialects.postgresql import JSONB
from core.models import Installation, InstallationFile
from core.services.distributors import get_distributor_from_user
from core.schemas.installations import InstallationCreatedNotification, InstallationApprovedNotification
from core.models import Client, Distributor, DistributorList, Equipment, Installation, List_, Site, User, UserList


def search_installations(current_user: User, equipment_id: int, distributor_id: int, client_id: int, serial: str, status: str, page: int, per_page: int, sort_by: dict = None):
    '''Get installations'''

    order_by = Installation.id.desc()
    if sort_by:
        if sort_by['key'] == 'equipmentModelReference':
            order_by = func.concat(
                Equipment.model, ' - ', Equipment.reference).label('equipment_model_reference')
        elif sort_by['key'] == 'clientName':
            order_by = Client.name
        elif sort_by['key'] == 'serial':
            order_by = Installation.serial
        elif sort_by['key'] == 'installedDate':
            order_by = Installation.installed_date
        elif sort_by['key'] == 'expirationDate':
            order_by = Installation.expiration_date
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Installation.status != 'INACTIVE']
    if equipment_id:
        query.append(Installation.equipment_id == equipment_id)
    if distributor_id:
        query.append(Installation.distributor_id == distributor_id)
    if client_id:
        query.append(Installation.client_id == client_id)
    if serial:
        query.append(Installation.serial.ilike(f'%{serial}%'))
    if status:
        query.append(Installation.status == status)

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(Installation.distributor_id == distributor.id)

    total = db.session.query(Installation)\
        .filter(*query)\
        .count()
    return list(db.session.execute(
        db.session.query(
            *Installation.__table__.c,
            Client.name.label('client_name'),
            Distributor.name.label('distributor_name'),
            func.concat(Equipment.model, ' - ', Equipment.reference).label('equipment_model_reference'))
        .join(Equipment)
        .join(Client, Client.id == Installation.client_id)
        .join(Distributor, Distributor.id == Installation.distributor_id)
        .filter(*query)
        .order_by(order_by)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_installation_by_id(installation_id: int):
    '''Get installation by installation id'''

    distributor_site = aliased(Site)
    client_site = aliased(Site)

    return db.session.query(
        *Installation.__table__.c,
        func.concat(Equipment.model, ' - ',
                    Equipment.reference).label('equipment_model_reference'),
        Distributor.name.label('distributor_name'),
        Client.name.label('client_name'),
        client_site.name.label('site_client_name'),
        distributor_site.name.label('site_distributor_name'),
        func.array_agg(
            func.cast('{"originalName":"' + InstallationFile.original_name + '","path":"' +
                      InstallationFile.path + '"}', JSON))
        .filter(InstallationFile.file_type == 'EVIDENCES')
        .label('installation_evidences_files'),
        func.cast(func.json_agg(
            func.cast('{"originalName":"' + InstallationFile.original_name + '","path":"' +
                      InstallationFile.path + '"}', JSON))
                  .filter(InstallationFile.file_type == 'SERIAL'), JSONB)[0]
        .label('installation_serial_file')
    )\
        .select_from(Installation)\
        .join(Equipment, Equipment.id == Installation.equipment_id)\
        .join(Distributor, Distributor.id == Installation.distributor_id)\
        .join(Client, Client.id == Installation.client_id)\
        .join(client_site, client_site.id == Installation.site_client_id)\
        .join(distributor_site, distributor_site.id == Installation.site_distributor_id)\
        .join(InstallationFile)\
        .filter(Installation.id == installation_id)\
        .group_by(*Installation.__table__.c,
                  'equipment_model_reference',
                  'distributor_name',
                  'client_name',
                  'site_client_name',
                  'site_distributor_name')\
        .first()


def check_installation_exists(installation_id: int):
    '''Check if installation exists'''

    return db.session.query(Installation).filter(Installation.id == installation_id).first()


def get_expiration_date(installed_date: str):
    '''
    Get expiration date from installed_date

    :param installed_date: Description
    :type installed_date: str
    '''

    fecha_dt = datetime.strptime(installed_date, "%b %d, %Y")
    return fecha_dt + timedelta(days=365 * 3)


def create_installation_file(installation_id: int, installation_file_data: FileStorage, file_type: str):
    '''Creates an installation file'''

    mimetype, extension, original_name, size = process_file(
        installation_file_data)
    hash_name = str(uuid.uuid4())
    file_path = f'./installations_files/{hash_name}{extension}'
    installation_file1 = InstallationFile(
        installation_id=installation_id,
        original_name=original_name,
        hash_name=hash_name,
        path=file_path,
        mimetype=mimetype,
        extension=extension,
        size=size,
        file_type=file_type
    )
    db.session.add(installation_file1)
    installation_file_data.save(file_path)


def create_installation(current_user: User, data: dict):
    '''Creates an installation'''

    serial_picture: FileStorage = data.pop('serial_picture')
    installation_pictures: list[FileStorage] = data.pop(
        'installation_pictures')

    data['user_id'] = current_user.id
    data['expiration_date'] = get_expiration_date(data['installed_date'])

    installation = Installation(**data)

    db.session.add(installation)
    db.session.flush()

    create_installation_file(installation.id, serial_picture, 'SERIAL')

    for installation_picture in installation_pictures:
        create_installation_file(
            installation.id, installation_picture, 'EVIDENCES')

    db.session.commit()
    return installation


def notify_creation(installation: Installation = None):
    '''Send notification to every admin that manages the distributor that creates an installation'''

    installation_data = InstallationCreatedNotification().dump(
        get_installation_by_id(installation.id))
    installation_files_attachments = [
        {
            'path': installation_data['serial_file']['path'],
            'filename': installation_data['serial_file']['originalName']
        },
        *[{'path': evidence['path'], 'filename': evidence['originalName']} for evidence in installation_data['evidences_files']]
    ]
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation.distributor_id, User.status == 'ACTIVE', User.role == 'ADMIN'))\
        .distinct(User.email)\
        .order_by(User.email)\
        .all()

    users_emails_by_language = {'es': [], 'en': []}
    for each_user in users_:
        users_emails_by_language[each_user.language].append(
            each_user.email)

    for each_language in users_emails_by_language.keys():
        users_filtered = users_emails_by_language[each_language]
        if len(users_filtered) > 0:
            with force_locale(each_language):
                mail_subject = gettext(u'SOE Latam - Registro de certificado de instalación #%(id)s',
                                       id=installation.id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='register_installation.html',
                params=installation_data,
                attachments=installation_files_attachments,
                language=each_language)


def is_installation_approved(installation_id: int):
    '''Check if installation is approved'''

    return db.session.query(Installation)\
        .filter(and_(Installation.id == installation_id, Installation.status == 'APPROVED'))\
        .first()


def update_installation(installation_id: int, data: dict):
    '''Update installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException(gettext('installationNotFound'))

    # Check if installation is not approved
    if is_installation_approved(installation_id):
        raise HTTPException(gettext('installationAlreadyApproved'))

    serial_picture: FileStorage = data.pop(
        'serial_picture') if 'serial_picture' in data else None
    installation_pictures: list[FileStorage] = data.pop(
        'installation_pictures') if 'installation_pictures' in data else None

    if 'installed_date' in data and data['installed_date']:
        data['expiration_date'] = get_expiration_date(data['installed_date'])

    if serial_picture:
        serial_picture_data = db.session.query(InstallationFile).filter(
            InstallationFile.installation_id == installation_id, InstallationFile.file_type == 'SERIAL').first()
        serial_picture.save(serial_picture_data.path)

    if installation_pictures:
        db.session.query(InstallationFile).filter(InstallationFile.installation_id ==
                                                  installation_id, InstallationFile.file_type == 'EVIDENCES').delete()
        for installation_picture in installation_pictures:
            create_installation_file(
                installation_id, installation_picture, 'EVIDENCES')

    db.session.merge(Installation(**data))
    db.session.commit()


def notify_update(installation_id: int):
    '''Notify admins the installation have been updated'''

    installation_data = InstallationApprovedNotification().dump(
        get_installation_by_id(installation_id))
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation_data['distributor_id'], User.status == 'ACTIVE', User.role == 'ADMIN'))\
        .distinct(User.email)\
        .order_by(User.email)\
        .all()

    users_emails_by_language = {'es': [], 'en': []}
    for each_user in users_:
        users_emails_by_language[each_user.language].append(
            each_user.email)

    for each_language in users_emails_by_language.keys():
        users_filtered = users_emails_by_language[each_language]
        if len(users_filtered) > 0:
            with force_locale(each_language):
                mail_subject = gettext(u'SOE Latam - Actualización de certificado de instalación #%(id)s',
                                       id=installation_id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='installation_updated.html',
                params=installation_data,
                language=each_language)


def delete_installation(installation_id: int):
    '''Delete installation'''

    db.session.merge(Installation(id=installation_id, status='INACTIVE'))
    db.session.commit()


def approve_installation(installation_id: int):
    '''Approve installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException(gettext('installationNotFound'))

    db.session.merge(Installation(id=installation_id, status='APPROVED'))
    db.session.commit()


def notify_approval(installation_id: int):
    '''Send notification to every distributor user about the installation approved'''

    installation_data: dict = InstallationApprovedNotification().dump(
        get_installation_by_id(installation_id))
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation_data['distributor_id'], User.status == 'ACTIVE', User.role != 'ADMIN'))\
        .distinct(User.email)\
        .order_by(User.email)\
        .all()

    users_emails_by_language = {'es': [], 'en': []}
    for each_user in users_:
        users_emails_by_language[each_user.language].append(
            each_user.email)

    for each_language in users_emails_by_language.keys():
        users_filtered = users_emails_by_language[each_language]
        if len(users_filtered) > 0:
            with force_locale(each_language):
                mail_subject = gettext(u'SOE Latam - Aprobación de instalación #%(id)s',
                                       id=installation_id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='installation_approved.html',
                params=installation_data,
                language=each_language)


def reject_installation(installation_id: int):
    '''Reject installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException(gettext('installationNotFound'))

    db.session.merge(Installation(id=installation_id, status='REJECTED'))
    db.session.commit()


def notify_rejection(installation_id: int, reject_comments: str):
    '''Send notification to every distributor user about the installation rejected'''

    installation_data: dict = InstallationApprovedNotification().dump(
        get_installation_by_id(installation_id))
    installation_data['reject_comments'] = reject_comments
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation_data['distributor_id'], User.status == 'ACTIVE', User.role != 'ADMIN'))\
        .distinct(User.email)\
        .order_by(User.email)\
        .all()
    users_emails_by_language = {'es': [], 'en': []}
    for each_user in users_:
        users_emails_by_language[each_user.language].append(
            each_user.email)

    for each_language in users_emails_by_language.keys():
        users_filtered = users_emails_by_language[each_language]
        if len(users_filtered) > 0:
            with force_locale(each_language):
                mail_subject = gettext(u'SOE Latam - Rechazo de instalación #%(id)s',
                                       id=installation_id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='installation_rejected.html',
                params=installation_data,
                language=each_language)
