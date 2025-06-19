import uuid
from core.app import db
from core.models import DistributorList, Installation, List_, User, UserList
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from core.models import Installation, InstallationFile


def get_installations(search: str, page: int, per_page: int):
    '''Get installations'''

    query = Installation.status == 'ACTIVE'
    # if search:
    #     query = and_(Installation.status == 'ACTIVE',
    #                  or_(Installation.equipment_id.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Installation).filter(query),
                       page=page, per_page=per_page, count=True)


def get_installation_by_id(installation_id: int):
    '''Get installation by installation id'''

    return db.session.query(Installation).filter(Installation.id == installation_id).first()


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


def send_notification(distributor_id):
    '''Send notification to every admin that manages the distributor that creates an installation'''

    # distributor_id = installation.distributor_id

    users_ = db.session.execute(
        db.session.query(User.email)
        .join(UserList)
        .join(List_)
        .join(DistributorList)
        .where(DistributorList.id == distributor_id)
    )
    users_emails = [user_data[0] for user_data in users_]

    
    


def update_installation(installation_id: int, installation_load):
    '''Update installation'''

    if not check_installation_exists(installation_id):
        raise HTTPException('Installation not found')

    db.session.merge(installation_load)
    db.session.commit()


def delete_installation(installation_id: int):
    '''Delete installation'''

    db.session.merge(Installation(id=installation_id, status='INACTIVE'))
    db.session.commit()
