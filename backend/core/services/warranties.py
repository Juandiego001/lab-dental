from datetime import datetime

from core.app import db
from core.models import Distributor, Equipment, User, Warranty, WarrantyReason
from sqlalchemy import or_, and_, JSON, and_, func
from bcrypt import checkpw
from werkzeug.exceptions import HTTPException

from core.services.distributors import get_distributor_from_user


def get_warranties(current_user: User, distributor_id: int, equipment_id: int, sale_date: datetime, invoice: str, status: str, page: int, per_page: int, sort_by: dict = None):
    '''Get warranties'''

    order_by = Warranty.id.desc()
    if sort_by:
        if sort_by['key'] == 'equipmentModelReference':
            order_by = func.concat(
                Equipment.model, ' - ', Equipment.reference).label('equipment_model_reference')
        elif sort_by['key'] == 'invoice':
            order_by = Warranty.invoice
        elif sort_by['key'] == 'saleDate':
            order_by = Warranty.sale_date
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Warranty.status != 'INACTIVE']
    if equipment_id:
        query.append(Warranty.equipment_id == equipment_id)
    if distributor_id:
        query.append(Warranty.distributor_id == distributor_id)
    if invoice:
        query.append(Warranty.invoice.ilike(f'%{invoice}%'))
    if sale_date:
        query.append(Warranty.sale_date == sale_date)
    if status:
        query.append(Warranty.status == status)
    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(Warranty.distributor_id == distributor.id)

    total = db.session.query(Warranty)\
        .filter(*query)\
        .count()
    return list(db.session.execute(
        db.session.query(
            Warranty.id,
            Warranty.invoice,
            Warranty.sale_date,
            Warranty.shipt_to,
            Warranty.problem,
            Warranty.solution,
            Warranty.status,
            Distributor.name.label('distributor_name'),
            func.concat(Equipment.model, ' - ', Equipment.reference).label('equipment_model_reference'))
        .join(Equipment, Equipment.id == Warranty.equipment_id)
        .join(Distributor, Distributor.id == Warranty.distributor_id)
        .filter(*query)
        .order_by(order_by)
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_warranty_by_id(warranty_id: int):
    '''Get warranty by warranty id'''

    return db.session.query(Warranty).filter(Warranty.id == warranty_id).first()


def check_warranty_exists(warranty_id: int):
    '''Check if warranty exists'''

    return db.session.query(Warranty).filter(Warranty.id == warranty_id).first()


def update_warranty(warranty_id: int, warranty_load):
    '''Update warranty'''

    if not check_warranty_exists(warranty_id):
        raise HTTPException('Warranty not found')

    db.session.merge(warranty_load)
    db.session.commit()


def delete_warranty(warranty_id: int):
    '''Delete warranty'''

    db.session.merge(Warranty(id=warranty_id, status='INACTIVE'))
    db.session.commit()


def create_warranty(warranty: dict):
    '''Create warranty'''

    reasons_ids = warranty.pop('reasons_ids')

    new_warranty = Warranty(**warranty)
    db.session.add(new_warranty)
    db.session.flush()

    for reason_id in reasons_ids:
        db.session.add(WarrantyReason(
            warranty_id=new_warranty.id, reason_id=reason_id))

    db.session.commit()
