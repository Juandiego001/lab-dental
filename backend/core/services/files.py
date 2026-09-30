
import os
from pathlib import Path
from core.models import EquipmentFile, InstallationFile, ManualFile, WarrantyFile
from core.app import db


default_mimetype = 'image/svg+xml'
default_equipment_img = Path('./default_imgs/car-wrench.svg')
default_manual_img = Path('./default_imgs/missing.svg')
default_installation_img = Path('./default_imgs/missing_grey.svg')
default_warranty_img = Path('./default_imgs/missing_grey.svg')


def get_user_file(photo: str):
    '''Get user file'''

    str_file_path = f'./users_files/{photo}'
    file_path = Path(str_file_path)
    if file_path.exists() and file_path.is_file():
        return file_path.resolve()
    else:
        return Path('./default_imgs/account.svg').resolve()


def get_equipment_file(hash_name: str):
    '''Get equipment file'''

    equipment_file = db.session.query(EquipmentFile)\
        .filter(EquipmentFile.hash_name == hash_name)\
        .first()

    if not equipment_file:
        return default_equipment_img.resolve(), default_mimetype

    str_file_path = f'./equipments_files/{equipment_file.hash_name}{equipment_file.extension}'
    file_path = Path(str_file_path)
    if file_path.exists() and file_path.is_file():
        return file_path.resolve(), equipment_file.mimetype
    else:
        return default_equipment_img.resolve(), default_mimetype


def get_manual_file(hash_name: str):
    '''Get manual file'''

    manual_file = db.session.query(ManualFile)\
        .filter(ManualFile.hash_name == hash_name)\
        .first()

    if not manual_file:
        return default_manual_img.resolve(), default_mimetype

    str_file_path = f'./manuals_files/{manual_file.hash_name}{manual_file.extension}'
    file_path = Path(str_file_path)
    if file_path.exists() and file_path.is_file():
        return file_path.resolve(), manual_file.mimetype
    else:
        return default_manual_img.resolve(), default_mimetype


def get_installation_file(hash_name: str):
    '''Get installation file'''

    installation_file = db.session.query(InstallationFile)\
        .filter(InstallationFile.hash_name == hash_name)\
        .first()

    if not installation_file:
        return default_installation_img.resolve(), default_mimetype

    str_file_path = f'./installations_files/{installation_file.hash_name}{installation_file.extension}'
    file_path = Path(str_file_path)
    if file_path.exists() and file_path.is_file():
        return file_path.resolve(), installation_file.mimetype
    else:
        return default_installation_img.resolve(), default_mimetype


def get_warranty_file(hash_name: str):
    '''Get warranty file'''

    warranty_file = db.session.query(WarrantyFile)\
        .filter(WarrantyFile.hash_name == hash_name)\
        .first()

    if not warranty_file:
        return default_warranty_img.resolve(), default_mimetype

    str_file_path = f'./warranties_files/{warranty_file.hash_name}{warranty_file.extension}'
    file_path = Path(str_file_path)
    if file_path.exists() and file_path.is_file():
        return file_path.resolve(), warranty_file.mimetype
    else:
        return default_warranty_img.resolve(), default_mimetype
