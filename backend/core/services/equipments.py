import uuid
from core.app import db
from pathlib import Path
from datetime import datetime
from core.utils import process_file
from werkzeug.exceptions import HTTPException
from sqlalchemy import and_, or_, literal, func
from werkzeug.datastructures import FileStorage
from core.models import Brand, Category, Equipment, EquipmentFile


def search_equipments(equipment_id: int, brand_id: int, category_id: int, model: str, reference: str, with_picture: bool, model_reference: str, page: int, per_page: int, sort_by: dict = None):
    '''
    Docstring for search_equipments

    :param brand_id: Description
    :type brand_id: int
    :param category_id: Description
    :type category_id: int
    :param model: Description
    :type model: str
    :param reference: Description
    :type reference: str
    '''

    order_by = Equipment.id.desc()
    if sort_by:
        if sort_by['key'] == 'model':
            order_by = Equipment.model
        elif sort_by['key'] == 'reference':
            order_by = Equipment.reference
        elif sort_by['key'] == 'brandName':
            order_by = Brand.name
        elif sort_by['key'] == 'categoryName':
            order_by = Category.name
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Equipment.status == 'ACTIVE']
    with_equipment_id = None

    if brand_id:
        query.append(Brand.id == brand_id)
    if category_id:
        query.append(Category.id == category_id)
    if model:
        query.append(Equipment.model.ilike(f'%{model}%'))
    if reference:
        query.append(Equipment.reference.ilike(f'%{reference}%'))
    if model_reference:
        query.append(or_(
            Equipment.model.ilike(f'%{model_reference}%'),
            literal(model_reference).ilike(
                '%' + Equipment.model + '%'),
            Equipment.reference.ilike(f'%{model_reference}%'),
            literal(model_reference).ilike('%' + Equipment.reference + '%')))

    select_cols = [
        *Equipment.__table__.c,
        func.concat(Equipment.model, ' - ',
                    Equipment.reference).label('model_reference'),
        Brand.name.label('brand_name'),
        Category.name.label('category_name')
    ]

    if with_picture:
        timestamp = int(datetime.now().timestamp())
        select_cols.append(
            EquipmentFile.path.concat(
                f'&v={timestamp}'
            ).label('main_picture')
        )
        select_cols.append(EquipmentFile.extension.label('extension'))
        query_stmt = db.session.query(*select_cols)\
            .join(Brand)\
            .join(Category)\
            .outerjoin(EquipmentFile, and_(
                EquipmentFile.equipment_id == Equipment.id,
                EquipmentFile.sort_order == 1,
                EquipmentFile.status == 'ACTIVE'
            ))
    else:
        query_stmt = db.session.query(*select_cols)\
            .join(Brand)\
            .join(Category)

    if equipment_id:
        query.append(Equipment.id != equipment_id)
        with_equipment_id =\
            query_stmt\
            .filter(Equipment.id == equipment_id)\
            .all()

    total = db.session.query(Equipment)\
        .join(Brand, Brand.id == Equipment.brand_id)\
        .join(Category, Category.id == Equipment.category_id)\
        .filter(*query).count()
    total += len(with_equipment_id) if with_equipment_id else 0

    equipments = list(db.session.execute(
        query_stmt
        .filter(*query)
        .order_by(order_by)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique())

    if not with_equipment_id:
        return equipments, total
    return with_equipment_id + equipments, total


def get_equipment_by_id(equipment_id: int):
    '''Get equipment by equipment id'''

    return db.session.query(
        *Equipment.__table__.c,
        Brand.name.label('brand_name'),
        Category.name.label('category_name'))\
        .join(Brand)\
        .join(Category)\
        .filter(Equipment.id == equipment_id)\
        .first()


def check_equipment_exists(equipment_id: int):
    '''Check if equipment exists'''

    return db.session.query(Equipment).filter(Equipment.id == equipment_id).first()


def create_equipment_file(equipment_id: int, equipment_file: FileStorage, sort_order: int):
    '''Creates an equipment file'''

    mimetype, extension, original_name, size = process_file(
        equipment_file)
    hash_name = str(uuid.uuid4())
    file_path = f'./equipments_files/{hash_name}{extension}'
    new_equipment_file = EquipmentFile(
        equipment_id=equipment_id,
        original_name=original_name,
        hash_name=hash_name,
        path=file_path,
        mimetype=mimetype,
        extension=extension,
        size=size,
        sort_order=sort_order,
    )
    db.session.add(new_equipment_file)
    equipment_file.save(file_path)


def create_equipment(data: dict):
    '''Create equipment'''

    equipment = Equipment(**data)
    db.session.add(equipment)
    db.session.commit()


def remove_equipment_file(equipment_file_id: int):
    '''Remove equipment file'''

    equipment_file = db.session.query(EquipmentFile)\
        .filter(
        EquipmentFile.id == equipment_file_id,
        EquipmentFile.status == 'ACTIVE'
    )\
        .first()
    try:
        Path(equipment_file.path).unlink(missing_ok=True)
    except Exception as e:
        print(
            f"Ocurrió un error al intentar eliminar el archivo: {e}")

    db.session.query(EquipmentFile).filter(
        EquipmentFile.equipment_id == equipment_file.equipment_id,
        EquipmentFile.status == 'ACTIVE',
        EquipmentFile.sort_order > equipment_file.sort_order,
    ).update(
        {"sort_order": EquipmentFile.sort_order - 1},
        synchronize_session=False
    )

    equipment_file.status = 'INACTIVE'
    db.session.merge(equipment_file)
    db.session.commit()


def update_equipment(equipment_id: int, equipment_data: dict):
    '''Update equipment'''

    if not check_equipment_exists(equipment_id):
        raise HTTPException('Equipment not found')

    equipment = Equipment(**equipment_data)
    db.session.merge(equipment)
    db.session.commit()


def delete_equipment(equipment_id: int):
    '''Delete equipment'''

    db.session.merge(Equipment(id=equipment_id, status='INACTIVE'))
    db.session.commit()


def search_equipment_files(equipment_id: int, title: str, description: str, original_name: str, extension: str, page: int, per_page: int):
    '''Search equipment files'''

    query = [EquipmentFile.status == 'ACTIVE',
             EquipmentFile.equipment_id == equipment_id]
    if title:
        query.append(EquipmentFile.title.ilike(f'%{title}%'))
    if description:
        query.append(EquipmentFile.description.ilike(f'%{description}%'))
    if original_name:
        query.append(EquipmentFile.original_name.ilike(f'%{original_name}%'))
    if extension:
        query.append(EquipmentFile.extension.ilike(f'%{extension}%'))

    total = db.session.query(EquipmentFile)\
        .filter(*query)\
        .count()
    equipment_files = db.session.query(EquipmentFile)\
        .filter(*query)\
        .order_by(EquipmentFile.sort_order.asc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    return equipment_files, total


def add_files(equipment_id: int, files: list[FileStorage]):
    '''Add equipment files'''

    max_sort_order = db.session.query(func.max(EquipmentFile.sort_order))\
        .filter(
            EquipmentFile.equipment_id == equipment_id,
            EquipmentFile.status == 'ACTIVE'
    ).scalar()
    next_sort_order: int = (max_sort_order or 0) + 1

    for file in files:
        create_equipment_file(
            equipment_id=equipment_id,
            equipment_file=file,
            sort_order=next_sort_order
        )
        next_sort_order += 1
    db.session.commit()


def get_equipment_file(file_id: int):
    '''Get equipment file'''

    return db.session.query(EquipmentFile)\
        .filter(EquipmentFile.id == file_id)\
        .first()


def update_equipment_file(file_id: int, data: dict):
    '''Update equipment file'''

    db.session.merge(EquipmentFile(id=file_id, **data))
    db.session.commit()


def update_equipment_file_order(equipment_id: int, file_id: int, new_sort_order: int):
    '''Update equipment file order'''

    target_file = db.session.query(EquipmentFile).filter(
        EquipmentFile.id == file_id,
        EquipmentFile.equipment_id == equipment_id,
        EquipmentFile.status == 'ACTIVE'
    ).first()

    if not target_file:
        return

    old_sort_order = target_file.sort_order

    if old_sort_order == new_sort_order:
        return

    if new_sort_order < old_sort_order:
        db.session.query(EquipmentFile).filter(
            EquipmentFile.equipment_id == equipment_id,
            EquipmentFile.status == 'ACTIVE',
            EquipmentFile.sort_order >= new_sort_order,
            EquipmentFile.sort_order < old_sort_order
        ).update(
            {"sort_order": EquipmentFile.sort_order + 1},
            synchronize_session=False
        )

    elif new_sort_order > old_sort_order:
        db.session.query(EquipmentFile).filter(
            EquipmentFile.equipment_id == equipment_id,
            EquipmentFile.status == 'ACTIVE',
            EquipmentFile.sort_order > old_sort_order,
            EquipmentFile.sort_order <= new_sort_order
        ).update(
            {"sort_order": EquipmentFile.sort_order - 1},
            synchronize_session=False
        )

    target_file.sort_order = new_sort_order

    try:
        db.session.commit()
        return {"message": "Orden actualizado correctamente"}
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando el orden: {e}")
        return {"error": "Ocurrió un problema al guardar el orden"}
