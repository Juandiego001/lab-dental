from datetime import datetime
import io

from weasyprint import HTML

from core.app import db, FRONTEND_APP_BASE_URL
from core.models import Address, City, Contact, Country, Distributor, DistributorList, Equipment, List_, Reason, Site, User, UserList, Warranty, WarrantyReason
from sqlalchemy import delete, and_, and_, func
from werkzeug.exceptions import HTTPException
from flask.templating import render_template
from flask_babel import force_locale, gettext
from core.utils import send_mail
from core.schemas.warranties import WarrantyPDF
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

    return db.session.query(
        Distributor.id.label('distributor_id'),
        func.array_agg(WarrantyReason.reason_id).label('reasons_ids'),
        Warranty.id,
        Warranty.invoice,
        Warranty.sale_date,
        Warranty.shipt_to,
        Warranty.problem,
        Warranty.solution,
        Warranty.status,
        Warranty.parts,

        # Contact data
        func.jsonb_build_object(
            'id', Contact.id,
            'email', Contact.email,
            'position', Contact.position,
            'full_name', Contact.full_name
        ).label('contact'),

        # Site data
        func.jsonb_build_object(
            'id', Site.id,
            'address_id', Site.address_id,
            'name', Site.name
        ).label('site'),

        # Equipment data
        func.jsonb_build_object(
            'id', Equipment.id,
            'category_id', Equipment.category_id,
            'model', Equipment.model,
            'reference', Equipment.reference
        ).label('equipment'),
    )\
        .join(Distributor, Distributor.id == Warranty.distributor_id)\
        .join(Site, Site.id == Warranty.site_id)\
        .join(Contact, Contact.id == Warranty.contact_id)\
        .join(Equipment, Equipment.id == Warranty.equipment_id)\
        .join(WarrantyReason, WarrantyReason.warranty_id == Warranty.id)\
        .filter(Warranty.id == warranty_id)\
        .group_by(Distributor.id, Site.id, Contact.id, Equipment.id, Warranty.id)\
        .first()


def get_warranty_by_id_for_pdf(warranty_id: int):
    '''Get warranty by warranty id for PDF generation'''

    return db.session.query(
        Distributor.name.label('distributor'),
        func.array_agg(Reason.name).label('reasons_names'),
        Warranty.invoice,
        Warranty.sale_date,
        Warranty.shipt_to,
        Warranty.problem,
        Warranty.solution,
        Warranty.status,
        Warranty.parts,

        # Contact data
        func.jsonb_build_object(
            'email', Contact.email,
            'position', Contact.position,
            'full_name', Contact.full_name
        ).label('contact'),

        # Site data
        func.jsonb_build_object(
            'address', Address.description,
            'city', City.name,
            'country', Country.name
        ).label('site'),

        # Equipment data
        func.jsonb_build_object(
            'model', Equipment.model,
            'reference', Equipment.reference
        ).label('equipment')
    )\
        .select_from(Warranty)\
        .join(Distributor, Distributor.id == Warranty.distributor_id)\
        .join(Site, Site.id == Warranty.site_id)\
        .join(Address, Address.id == Site.address_id)\
        .join(City, City.id == Address.city_id)\
        .join(Country, Country.id == Address.country_id)\
        .join(Contact, Contact.id == Warranty.contact_id)\
        .join(Equipment, Equipment.id == Warranty.equipment_id)\
        .join(WarrantyReason, WarrantyReason.warranty_id == Warranty.id)\
        .join(Reason, Reason.id == WarrantyReason.reason_id)\
        .filter(Warranty.id == warranty_id)\
        .group_by(
            Distributor.name,
            Warranty.invoice,
            Warranty.sale_date,
            Warranty.shipt_to,
            Warranty.problem,
            Warranty.solution,
            Warranty.status,
            Warranty.parts,
            Contact.email,
            Contact.position,
            Contact.full_name,
            Address.description,
            City.name,
            Country.name,
            Equipment.model,
            Equipment.reference,
    )\
        .first()


def check_warranty_exists(warranty_id: int):
    '''Check if warranty exists'''

    return db.session.query(Warranty).filter(Warranty.id == warranty_id).first()


def update_warranty(warranty_id: int, json_data: dict):
    '''Update warranty'''

    if not check_warranty_exists(warranty_id):
        raise HTTPException('Warranty not found')

    reasons_ids = json_data.pop('reasons_ids')

    # Delete warranty reasons
    db.session.execute(delete(WarrantyReason).where(
        WarrantyReason.warranty_id == warranty_id))

    # Insert warranty reasons again
    reasons_ids_updated = [WarrantyReason(
        warranty_id=warranty_id, reason_id=reason_id) for reason_id in reasons_ids]
    db.session.add_all(reasons_ids_updated)
    db.session.merge(Warranty(id=warranty_id, **json_data))

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


def group_reasons(reasons: list):
    '''Group reasons for PDF print'''

    counter = 0
    group_level = 0
    grouped_reasons = [[]]
    for reason in reasons:
        if counter < 2:
            counter += 1
            grouped_reasons[group_level].append(reason)
        else:
            counter = 0
            grouped_reasons[group_level].append(reason)
            grouped_reasons.append([])
            group_level += 1

    return grouped_reasons


def numeric_format_parts(parts: list[dict]) -> tuple[float, list]:
    '''Numeric format parts'''

    total_price = 0
    formatted_parts = []
    for part in parts:
        total_price += int(part['quantity']) * float(part['price'])
        formatted_part = part
        if 'price' in formatted_part:
            formatted_part['price'] = f"${part['price']:,.2f}"
        else:
            formatted_part['price'] = "$0.0"

        if 'total' in formatted_part:
            formatted_part['total'] = f"${part['total']:,.2f}"
        else:
            formatted_part['total'] = "$0.0"

        formatted_parts.append(formatted_part)

    total_price = f"${total_price:,.2f}"
    return total_price, formatted_parts


def get_warranty_pdf(warranty_id: int):
    '''Get warranty PDF'''

    the_warranty = get_warranty_by_id_for_pdf(warranty_id)
    the_warranty: WarrantyPDF = WarrantyPDF().dump(the_warranty)
    total_price, formatted_parts = numeric_format_parts(the_warranty['parts'])
    grouped_reasons = group_reasons(the_warranty['reasons_names'])

    data = {
        **the_warranty,
        "date": datetime.now().strftime("%m/%d/%Y"),
        "distributor": the_warranty['distributor'],
        "grouped_reasons": grouped_reasons,
        "total_price": total_price,
        "parts": formatted_parts
    }

    pdf_rendered = render_template('warranties.html', **data)
    pdf_bytes = HTML(string=pdf_rendered).write_pdf()
    pdf_buffer = io.BytesIO(pdf_bytes)
    return pdf_buffer


def approve_warranty(warranty_id: int):
    '''Approve Warranty'''

    if not check_warranty_exists(warranty_id):
        raise HTTPException(gettext('warrantyNotFound'))

    db.session.merge(Warranty(id=warranty_id, status='APPROVED'))
    db.session.commit()


def notify_approval(warranty_id: int):
    '''Send notification to every distributor user about the warranty approved'''

    warranty_data: dict = WarrantyPDF().dump(
        get_warranty_by_id_for_pdf(warranty_id))
    total_price, formatted_parts = numeric_format_parts(warranty_data['parts'])
    warranty_data = {
        **warranty_data,
        "date": datetime.now().strftime("%m/%d/%Y"),
        "distributor": warranty_data['distributor'],
        "reasons": warranty_data['reasons_names'],
        "total_price": total_price,
        "parts": formatted_parts,
        "app_url": f'{FRONTEND_APP_BASE_URL}/app/warranties'
    }

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .join(Warranty, Warranty.distributor_id == DistributorList.distributor_id)\
        .filter(and_(Warranty.id == warranty_id, User.status == 'ACTIVE', User.role != 'ADMIN'))\
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
                mail_subject = gettext(u'SOE Latam - Aprobación de garantía #%(id)s',
                                       id=warranty_id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='warranty_approved.html',
                params=warranty_data,
                language=each_language)


def reject_warranty(warranty_id: int):
    '''Reject warranty'''

    if not check_warranty_exists(warranty_id):
        raise HTTPException(gettext('warrantyNotFound'))

    db.session.merge(Warranty(id=warranty_id, status='REJECTED'))
    db.session.commit()


def notify_rejection(warranty_id: int, reject_comments: str):
    '''Send notification to every distributor user about the installation rejected'''

    warranty_data: dict = WarrantyPDF().dump(
        get_warranty_by_id_for_pdf(warranty_id))
    total_price, formatted_parts = numeric_format_parts(warranty_data['parts'])
    warranty_data = {
        **warranty_data,
        "date": datetime.now().strftime("%m/%d/%Y"),
        "distributor": warranty_data['distributor'],
        "reasons": warranty_data['reasons_names'],
        "total_price": total_price,
        "parts": formatted_parts,
        "app_url": f'{FRONTEND_APP_BASE_URL}/app/warranties',
        "reject_comments": reject_comments
    }

    users_ = db.session.query(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .join(Warranty, Warranty.distributor_id == DistributorList.distributor_id)\
        .filter(and_(Warranty.id == warranty_id, User.status == 'ACTIVE', User.role != 'ADMIN'))\
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
                mail_subject = gettext(u'SOE Latam - Rechazo de garantía #%(id)s',
                                       id=warranty_id)
            send_mail(
                subject=mail_subject,
                to=users_filtered,
                plantilla='warranty_rejected.html',
                params=warranty_data,
                language=each_language)
