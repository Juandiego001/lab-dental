from core.app import db
from core.models import Brand, Category, Equipment
from sqlalchemy import and_, or_, literal, func
from werkzeug.exceptions import HTTPException


def search_equipments(equipment_id: int, brand_id: int, category_id: int, model: str, reference: str, with_picture: bool, model_reference: str, page: int, per_page: int):
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

    query_stmt = db.session.query(
        *Equipment.__table__.c,
        func.concat(Equipment.model, ' - ',
                    Equipment.reference).label('model_reference'),
        Brand.name.label('brand_name'),
        Category.name.label('category_name'))\
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
        .order_by(Equipment.id.desc())
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


def update_equipment(equipment_id: int, equipment_load):
    '''Update equipment'''

    if not check_equipment_exists(equipment_id):
        raise HTTPException('Equipment not found')

    db.session.merge(equipment_load)
    db.session.commit()


def delete_equipment(equipment_id: int):
    '''Delete equipment'''

    db.session.merge(Equipment(id=equipment_id, status='INACTIVE'))
    db.session.commit()
