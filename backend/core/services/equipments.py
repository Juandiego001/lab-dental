import uuid
from pathlib import Path
from core.app import db
from core.utils import process_file
from sqlalchemy import and_, or_, literal, func
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from core.models import Brand, Category, Equipment, EquipmentFile
from datetime import datetime


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

        query_stmt = db.session.query(*select_cols)\
            .join(Brand)\
            .join(Category)\
            .outerjoin(EquipmentFile, and_(
                EquipmentFile.equipment_id == Equipment.id,
                EquipmentFile.is_main == True,
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

    print('query_stmt: ')
    print(query_stmt)

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


def create_equipment_file(equipment_id: int, equipment_file: FileStorage, is_main: bool = False):
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
        is_main=is_main
    )
    db.session.add(new_equipment_file)
    equipment_file.save(file_path)


def create_equipment(data: dict):
    '''Create equipment'''

    main_picture = None
    if 'main_picture' in data:
        main_picture: FileStorage = data.pop('main_picture')

    secondary_pictures = None
    if 'secondary_pictures' in data:
        secondary_pictures: list[FileStorage] = data.pop('secondary_pictures')

    videos = None
    if 'videos' in data:
        videos: list[FileStorage] = data.pop('videos')

    equipment = Equipment(**data)
    db.session.add(equipment)
    db.session.flush()

    if main_picture:
        create_equipment_file(
            equipment_id=equipment.id,
            equipment_file=main_picture,
            is_main=True
        )

    if secondary_pictures:
        for picture in secondary_pictures:
            create_equipment_file(
                equipment_id=equipment.id,
                equipment_file=picture,
            )

    if videos:
        for video in videos:
            create_equipment_file(
                equipment_id=equipment.id,
                equipment_file=video,
            )

    db.session.commit()
    return equipment


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

    equipment_file.status = 'INACTIVE'
    db.session.merge(equipment_file)
    db.session.commit()


def update_equipment(equipment_id: int, equipment_data: dict):
    '''Update equipment'''

    if not check_equipment_exists(equipment_id):
        raise HTTPException('Equipment not found')

    main_picture = None
    if 'main_picture' in equipment_data:
        main_picture: FileStorage = equipment_data.pop('main_picture')

    secondary_pictures = None
    if 'secondary_pictures' in equipment_data:
        secondary_pictures: list[FileStorage] = equipment_data.pop(
            'secondary_pictures')

    videos = None
    if 'videos' in equipment_data:
        videos: list[FileStorage] = equipment_data.pop('videos')

    equipment = Equipment(**equipment_data)
    db.session.merge(equipment)

    if main_picture:
        existing_main_picture = db.session.query(EquipmentFile)\
            .filter(
                EquipmentFile.equipment_id == equipment_id,
                EquipmentFile.is_main == True,
                EquipmentFile.status == 'ACTIVE'
        )\
            .first()
        if existing_main_picture:
            main_picture.save(existing_main_picture.path)
        else:
            create_equipment_file(
                equipment_id=equipment.id,
                equipment_file=main_picture,
                is_main=True
            )

    if secondary_pictures:
        existing_secondary_pictures = db.session.query(EquipmentFile)\
            .filter(
                EquipmentFile.equipment_id == equipment_id,
                EquipmentFile.is_main == False,
                EquipmentFile.status == 'ACTIVE',
                EquipmentFile.extension != '.mp4'
        )\
            .all()

        # Remove existing secondary pictures
        if existing_secondary_pictures:
            for picture in existing_secondary_pictures:
                remove_equipment_file(picture.id)

        for picture in secondary_pictures:
            create_equipment_file(
                equipment_id=equipment.id,
                equipment_file=picture,
            )

    if videos:
        existing_videos = db.session.query(EquipmentFile)\
            .filter(
                EquipmentFile.equipment_id == equipment_id,
                EquipmentFile.is_main == False,
                EquipmentFile.status == 'ACTIVE',
                EquipmentFile.extension == '.mp4'
        )\
            .all()

        # Remove existing secondary pictures
        if existing_videos:
            for video in existing_videos:
                remove_equipment_file(video.id)

        for video in videos:
            create_equipment_file(
                equipment_id=equipment.id,
                equipment_file=video,
            )

    db.session.commit()
    return equipment


def delete_equipment(equipment_id: int):
    '''Delete equipment'''

    db.session.merge(Equipment(id=equipment_id, status='INACTIVE'))
    db.session.commit()


def get_equipment_files(equipment_id: int):
    '''Get equipment files'''

    equipment_files = db.session.query(EquipmentFile)\
        .join(Equipment, Equipment.id == EquipmentFile.equipment_id)\
        .filter(Equipment.id == equipment_id, EquipmentFile.status == 'ACTIVE')\
        .all()

    return {'equipment_files': equipment_files}
