import uuid
from core.app import db, FRONTEND_APP_BASE_URL
from core.utils import send_mail
from sqlalchemy.orm import aliased
from sqlalchemy import JSON, or_, and_, func
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from sqlalchemy.dialects.postgresql import JSONB
from core.models import Installation, InstallationFile
from core.schemas.installations import InstallationCreatedNotification, InstallationApprovedNotification
from core.models import Client, Distributor, DistributorList, Equipment, Installation, List_, Site, User, UserList


def get_installations(search: str, page: int, per_page: int):
    '''Get installations'''

    query = Installation.status != 'INACTIVE'
    if search:
        query = and_(Installation.status != 'INACTIVE',
                     or_(Installation.equipment_id.ilike(f'%{search}%')))

    total = db.session.query(Installation).count()

    return list(db.session.execute(
        db.session.query(
            *Installation.__table__.c,
            func.concat(Equipment.model, ' - ', Equipment.serial).label('equipment_serial_model'))
        .join(Equipment)
        .filter(query)
        .order_by(Installation.id.desc())
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
                    Equipment.serial).label('equipment_serial_model'),
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
        .label('installation_serial_file'),
        func.cast(func.json_agg(
            func.cast('{"originalName":"' + InstallationFile.original_name + '","path":"' +
                      InstallationFile.path + '"}', JSON))
                  .filter(InstallationFile.file_type == 'FORMAT'), JSONB)[0]
        .label('installation_format_file'),
    )\
        .select_from(Installation)\
        .join(Equipment)\
        .join(Distributor)\
        .join(Client)\
        .join(client_site, client_site.id == Installation.site_client_id)\
        .join(distributor_site, distributor_site.id == Installation.site_distributor_id)\
        .join(InstallationFile)\
        .filter(Installation.id == installation_id)\
        .group_by(*Installation.__table__.c,
                  'equipment_serial_model',
                  'distributor_name',
                  'client_name',
                  'site_client_name',
                  'site_distributor_name')\
        .first()


def check_installation_exists(installation_id: int):
    '''Check if installation exists'''

    return db.session.query(Installation).filter(Installation.id == installation_id).first()


def create_installation_file(installation_id: int, installation_file_data: FileStorage, file_type: str):
    '''Creates an installation file'''

    original_name = installation_file_data.filename
    _, extension = original_name.split('.')
    uuid_name = str(uuid.uuid4())
    file_path = f'./files_data/{uuid_name}.{extension}'
    installation_file1 = InstallationFile(
        installation_id=installation_id, name=original_name, original_name=original_name, path=file_path, file_type=file_type)
    db.session.add(installation_file1)
    installation_file_data.save(file_path)


def create_installation(data: dict):
    '''Creates an installation'''

    format_picture: FileStorage = data.pop('format_picture')
    serial_picture: FileStorage = data.pop('serial_picture')
    installation_pictures: list[FileStorage] = data.pop(
        'installation_pictures')

    data['user_id'] = 1
    installation = Installation(**data)

    db.session.add(installation)
    db.session.flush()

    create_installation_file(installation.id, format_picture, 'FORMAT')
    create_installation_file(installation.id, serial_picture, 'SERIAL')

    for installation_picture in installation_pictures:
        create_installation_file(
            installation.id, installation_picture, 'EVIDENCES')

    db.session.commit()
    return installation


def notify_creation(installation: Installation = None):
    '''Send notification to every admin that manages the distributor that creates an installation'''

    users_ = db.session.query(User.email).distinct(User.email)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation.distributor_id, User.status == 'ACTIVE', User.role == 'ADMIN')).all()

    users_emails = [user_data[0] for user_data in users_]

    # If there are users to notify
    if len(users_emails):
        installation_data = InstallationCreatedNotification().dump(
            get_installation_by_id(installation.id))
        installation_files_attachments = [
            {
                'path': installation_data['serial_file']['path'],
                'filename': installation_data['serial_file']['originalName']
            },
            {
                'path': installation_data['format_file']['path'],
                'filename': installation_data['format_file']['originalName']
            },
            *[{'path': evidence['path'], 'filename': evidence['originalName']} for evidence in installation_data['evidences_files']]
        ]
        installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

        send_mail(f'SOE Latam - Registro de certificado de instalación #{installation.id}',
                  users_emails, 'register_installation.html',
                  installation_data,
                  installation_files_attachments)


def update_installation(installation_id: int, data: dict):
    '''Update installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException('Installation not found')

    format_picture: FileStorage = data.pop(
        'format_picture') if 'format_picture' in data else None
    serial_picture: FileStorage = data.pop(
        'serial_picture') if 'serial_picture' in data else None
    installation_pictures: list[FileStorage] = data.pop(
        'installation_pictures') if 'installation_pictures' in data else None

    if format_picture:
        format_picture_data = db.session.query(InstallationFile).filter(
            InstallationFile.installation_id == installation_id, InstallationFile.file_type == 'FORMAT').first()
        format_picture.save(format_picture_data.path)

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


def delete_installation(installation_id: int):
    '''Delete installation'''

    db.session.merge(Installation(id=installation_id, status='INACTIVE'))
    db.session.commit()


def approve_installation(installation_id: int):
    '''Approve installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException('Installation not found')

    db.session.merge(Installation(id=installation_id, status='APPROVED'))
    db.session.commit()


def notify_approval(installation_id: int):
    '''Send notification to every distributor user about the installation approved'''

    installation_data: dict = InstallationApprovedNotification().dump(
        get_installation_by_id(installation_id))
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'

    users_ = db.session.query(User.email).distinct(User.email)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation_data['distributor_id'], User.status == 'ACTIVE', User.role != 'ADMIN'))\
        .all()

    users_emails = [user_data[0] for user_data in users_]

    # If there are users to notify
    if len(users_emails):
        send_mail(f'SOE Latam - Aprobación de instalación #{installation_id}',
                  ['juandiego14012003@gmail.com'], 'installation_approved.html',
                  installation_data)


def reject_installation(installation_id: int):
    '''Reject installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException('Installation not found')

    db.session.merge(Installation(id=installation_id, status='REJECTED'))
    db.session.commit()


def notify_rejection(installation_id: int, reject_comments: str):
    '''Send notification to every distributor user about the installation rejected'''

    installation_data: dict = InstallationApprovedNotification().dump(
        get_installation_by_id(installation_id))
    installation_data['reject_comments'] = reject_comments
    installation_data['app_url'] = f'{FRONTEND_APP_BASE_URL}/app/installations'


    users_ = db.session.query(User.email).distinct(User.email)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .filter(and_(DistributorList.distributor_id == installation_data['distributor_id'], User.status == 'ACTIVE', User.role != 'ADMIN'))\
        .all()

    users_emails = [user_data[0] for user_data in users_]

    # If there are users to notify
    if len(users_emails):
        send_mail(f'SOE Latam - Rechazo de instalación #{installation_id}',
                  ['juandiego14012003@gmail.com'], 'installation_rejected.html',
                  installation_data)