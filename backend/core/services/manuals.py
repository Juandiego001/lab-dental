from pathlib import Path
import uuid

from core.app import db
from core.models import Manual, ManualFile, ManualType
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from werkzeug.datastructures import FileStorage

from core.utils import process_file


def search_manuals(equipment_id: int, title: str, description: str, manual_type_id: int, original_name: str, extension: str, page: int, per_page: int, sort_by: dict = None):
    '''Search manuals'''

    order_by = Manual.id.desc()
    if sort_by:
        if sort_by['key'] == 'title':
            order_by = Manual.title
        elif sort_by['key'] == 'manualType.name':
            order_by = ManualType.name
        elif sort_by['key'] == 'manualFile.size':
            order_by = ManualFile.size
        elif sort_by['key'] == 'manualFile.extension':
            order_by = ManualFile.extension
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Manual.status == 'ACTIVE']
    if equipment_id:
        query.append(Manual.equipment_id == equipment_id)
    if title:
        query.append(Manual.title.ilike(f'%{title}%'))
    if description:
        query.append(Manual.description.ilike(f'%{description}%'))
    if manual_type_id:
        query.append(Manual.manual_type_id == manual_type_id)
    if original_name:
        query.append(ManualFile.original_name.ilike(f'%{original_name}%'))
    if extension:
        query.append(ManualFile.extension == extension)

    total = db.session.query(Manual)\
        .join(ManualFile)\
        .join(ManualType)\
        .filter(*query)\
        .count()
    manuals = db.session.query(Manual)\
        .options(
            joinedload(Manual.manual_file),
            joinedload(Manual.manual_type)
    )\
        .join(ManualFile)\
        .join(ManualType)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    return manuals, total


def add_manual_file(manual_id: int, manual_file: FileStorage):
    '''Add Manual File'''

    mimetype, extension, original_name, size = process_file(manual_file)
    hash_name = str(uuid.uuid4())
    file_path = f'./manuals_files/{hash_name}{extension}'
    new_manual_file = ManualFile(
        manual_id=manual_id,
        original_name=original_name,
        hash_name=hash_name,
        mimetype=mimetype,
        extension=extension,
        size=size
    )
    db.session.add(new_manual_file)
    manual_file.save(file_path)


def create_manual(data: dict):
    '''Create Manual'''

    file = data.pop('file')
    new_manual = Manual(**data)
    db.session.add(new_manual)
    db.session.flush()

    add_manual_file(
        manual_id=new_manual.id,
        manual_file=file
    )

    db.session.commit()


def get_manual(manual_id: int):
    '''Get manual'''

    return db.session.query(Manual)\
        .filter(Manual.id == manual_id)\
        .first()


def search_manual_types(name: str, slug: str, page: int, per_page: int, sort_by: dict = None):
    '''Search manual types'''

    order_by = ManualType.id.desc()
    if sort_by:
        if sort_by['key'] == 'name':
            order_by = ManualType.name
        elif sort_by['key'] == 'slug':
            order_by = ManualType.slug
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [ManualType.status == 'ACTIVE']
    if name:
        query.append(ManualType.name.ilike(f'%{name}%'))
    if slug:
        query.append(ManualType.slug.ilike(f'%{slug}%'))

    total = db.session.query(ManualType)\
        .filter(*query)\
        .count()
    manual_types = db.session.query(ManualType)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    return manual_types, total


def update_manual(manual_id: int, data: dict):
    '''Update manual'''

    updated_manual = Manual(id=manual_id, **data)
    db.session.merge(updated_manual)
    db.session.commit()


def delete_manual(manual_id: int):
    '''Delete manual'''

    manual_file = db.session.query(ManualFile)\
        .filter(ManualFile.manual_id == manual_id)\
        .first()
    try:
        Path(f'./manuals_files/{manual_file.hash_name}{manual_file.extension}')\
            .unlink(missing_ok=True)
    except Exception as e:
        print(
            f"Ocurrió un error al intentar eliminar el archivo: {e}")

    manual_file.status = 'INACTIVE'
    db.session.merge(Manual(id=manual_id, status='INACTIVE'))
    db.session.commit()
