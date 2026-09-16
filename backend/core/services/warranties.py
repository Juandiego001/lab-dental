from datetime import datetime, date
import io
import uuid
from pathlib import Path
from weasyprint import HTML
from werkzeug.datastructures import FileStorage
from core.app import db, FRONTEND_APP_BASE_URL
from core.models import Address, City, Contact, Country, Distributor, DistributorList, Equipment, List_, Reason, Site, State, User, UserList, Warranty, WarrantyFile, WarrantyReason, WarrantyWCO
from sqlalchemy import delete, and_, and_, func
from werkzeug.exceptions import HTTPException
from flask.templating import render_template
from flask_babel import force_locale, gettext
from core.utils import process_file, send_mail
from core.schemas.warranties import WarrantyPDF
from core.services.distributors import get_distributor_from_user


def get_warranties(current_user: User, distributor_id: int, equipment_id: int, wco_code: int, wco_year: int, sale_date: datetime, invoice: str, serial: str, status: str, page: int, per_page: int, sort_by: dict = None):
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
    if serial:
        query.append(Warranty.serial.ilike(f'%{serial}%'))
    if wco_code:
        query.append(WarrantyWCO.code == wco_code)
    if wco_year:
        query.append(WarrantyWCO.year == wco_year)
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
            WarrantyWCO.code.label('wco_code'),
            WarrantyWCO.year.label('wco_year'),
            Distributor.name.label('distributor_name'),
            func.concat(Equipment.model, ' - ', Equipment.reference).label('equipment_model_reference'))
        .join(Equipment, Equipment.id == Warranty.equipment_id)
        .join(Distributor, Distributor.id == Warranty.distributor_id)
        .outerjoin(WarrantyWCO, WarrantyWCO.warranty_id == Warranty.id)
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
        Warranty.serial,
        Warranty.sale_date,
        Warranty.shipt_to,
        Warranty.problem,
        Warranty.solution,
        Warranty.status,
        Warranty.parts,
        Warranty.received_at,
        WarrantyWCO.code.label('wco_code'),
        WarrantyWCO.year.label('wco_year'),

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
        .outerjoin(WarrantyWCO, WarrantyWCO.warranty_id == Warranty.id)\
        .filter(Warranty.id == warranty_id)\
        .group_by(Distributor.id, Site.id, Contact.id, Equipment.id, Warranty.id, WarrantyWCO.code, WarrantyWCO.year)\
        .first()


def get_warranty_by_id_for_pdf(warranty_id: int):
    '''Get warranty by warranty id for PDF generation'''

    return db.session.query(
        Distributor.name.label('distributor'),
        func.array_agg(Reason.name).label('reasons_names'),
        Warranty.invoice,
        Warranty.serial,
        Warranty.sale_date,
        Warranty.shipt_to,
        Warranty.problem,
        Warranty.solution,
        Warranty.status,
        Warranty.parts,
        Warranty.received_at,
        Warranty.approved_at,
        Warranty.approved_at,
        WarrantyWCO.code.label('wco_code'),
        WarrantyWCO.year.label('wco_year'),
        User.full_name.label('user'),

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
            'state', State.name,
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
        .outerjoin(City, City.id == Address.city_id)\
        .join(State, State.id == Address.state_id)\
        .join(Country, Country.id == Address.country_id)\
        .join(Contact, Contact.id == Warranty.contact_id)\
        .join(Equipment, Equipment.id == Warranty.equipment_id)\
        .join(WarrantyReason, WarrantyReason.warranty_id == Warranty.id)\
        .join(Reason, Reason.id == WarrantyReason.reason_id)\
        .outerjoin(User, User.id == Warranty.user_approval_id)\
        .outerjoin(WarrantyWCO, WarrantyWCO.warranty_id == Warranty.id)\
        .filter(Warranty.id == warranty_id)\
        .group_by(
            Distributor.name,
            Warranty.invoice,
            Warranty.serial,
            Warranty.sale_date,
            Warranty.shipt_to,
            Warranty.problem,
            Warranty.solution,
            Warranty.status,
            Warranty.parts,
            Warranty.received_at,
            Warranty.approved_at,
            WarrantyWCO.code,
            WarrantyWCO.year,
            User.full_name,
            Contact.email,
            Contact.position,
            Contact.full_name,
            Address.description,
            City.name,
            State.name,
            Country.name,
            Equipment.model,
            Equipment.reference,
    )\
        .first()


def check_warranty_exists(warranty_id: int) -> Warranty | None:
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


def create_warranty_file(warranty_id: int, warranty_file_data: FileStorage):
    '''Creates an warranty file'''

    mimetype, extension, original_name, size = process_file(warranty_file_data)
    hash_name = str(uuid.uuid4())
    file_path = f'./warranties_files/{hash_name}{extension}'
    warranty_file = WarrantyFile(
        warranty_id=warranty_id,
        original_name=original_name,
        hash_name=hash_name,
        path=file_path,
        mimetype=mimetype,
        extension=extension,
        size=size
    )
    db.session.add(warranty_file)
    warranty_file_data.save(file_path)


def create_warranty(warranty: dict):
    '''Create warranty'''

    warranty_files: list[FileStorage] = warranty.pop('warranty_files')
    reasons_ids = warranty.pop('reasons_ids')

    new_warranty = Warranty(**warranty)
    db.session.add(new_warranty)
    db.session.flush()

    for reason_id in reasons_ids:
        db.session.add(WarrantyReason(
            warranty_id=new_warranty.id, reason_id=reason_id))

    for warranty_file in warranty_files:
        create_warranty_file(new_warranty.id, warranty_file)

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


def get_warranty_pdf(warranty_id: int):
    '''Get warranty PDF'''

    the_warranty = get_warranty_by_id_for_pdf(warranty_id)
    the_warranty: WarrantyPDF = WarrantyPDF().dump(the_warranty)
    grouped_reasons = group_reasons(the_warranty['reasons_names'])

    data = {
        **the_warranty,
        "date": datetime.now().strftime('%B %d, %Y'),
        "distributor": the_warranty['distributor'],
        "grouped_reasons": grouped_reasons
    }

    pdf_rendered = render_template('warranties.html', **data)
    pdf_bytes = HTML(string=pdf_rendered).write_pdf()
    pdf_buffer = io.BytesIO(pdf_bytes)
    return pdf_buffer


def approve_warranty(current_user: User, warranty_id: int):
    '''Approve Warranty'''

    current_date = datetime.now()
    current_warranty = check_warranty_exists(warranty_id)
    if not current_warranty:
        raise HTTPException(gettext('warrantyNotFound'))

    '''Validation to check if warranty already have WCO'''
    existing_wco = db.session.query(WarrantyWCO)\
        .filter(WarrantyWCO.warranty_id == warranty_id).first()

    if not existing_wco:
        last_warranty_wco = db.session.query(WarrantyWCO)\
            .order_by(WarrantyWCO.id.desc())\
            .first()

        '''Validation for every new year'''
        '''Every time a year passes, the entered warranty code must reset to 1 again.'''
        current_year = date.today().year
        new_warranty_wco = WarrantyWCO(
            warranty_id=warranty_id,
            year=current_year
        )
        if not last_warranty_wco or last_warranty_wco.year < current_year:
            new_warranty_wco.code = 1
        else:
            new_warranty_wco.code = last_warranty_wco.code + 1

        db.session.add(new_warranty_wco)

    current_warranty.status = 'APPROVED'
    if not current_warranty.received_at:
        current_warranty.received_at = current_date

    current_warranty.user_approval_id = current_user.id
    current_warranty.approved_at = current_date
    db.session.commit()


def notify_approval(warranty_id: int):
    '''Send notification to every distributor user about the warranty approved'''

    warranty_data: dict = WarrantyPDF().dump(
        get_warranty_by_id_for_pdf(warranty_id))
    warranty_data = {
        **warranty_data,
        "date": datetime.now().strftime('%B %d, %Y'),
        "distributor": warranty_data['distributor'],
        "reasons": warranty_data['reasons_names'],
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

    # Se envía el correo para Pipe para Snapon
    warranty_files: list[WarrantyFile] = db.session.query(
        WarrantyFile).filter(WarrantyFile.warranty_id == warranty_id).all()
    grouped_reasons = group_reasons(warranty_data['reasons_names'])
    data = {
        **warranty_data,
        "date": datetime.now().strftime('%B %d, %Y'),
        "distributor": warranty_data['distributor'],
        "grouped_reasons": grouped_reasons
    }

    pdf_rendered = render_template('warranties.html', **data)
    pdf_bytes = HTML(string=pdf_rendered).write_pdf()

    send_mail(
        subject=f'Processing Warranty with WCO: {warranty_data['wco']}',
        to=['Andres.Leon@snapon.com'],
        plantilla='warranties_snapon_message.html',
        params={'wco': warranty_data['wco']},
        language='en',
        with_soe_logo=False,
        attachments=[
            {
                'filename': f"Warranty {warranty_data['wco']}.pdf",
                'content': pdf_bytes
            },
            *[{'path':  warranty_file.path, 'filename': warranty_file.original_name} for warranty_file in warranty_files]
        ]
    )


def reject_warranty(warranty_id: int):
    '''Reject warranty'''

    current_warranty = check_warranty_exists(warranty_id)
    if not current_warranty:
        raise HTTPException(gettext('warrantyNotFound'))

    current_warranty.status = 'REJECTED'
    current_warranty.user_approval_id = None
    current_warranty.approved_at = None
    db.session.commit()


def notify_rejection(warranty_id: int, reject_comments: str):
    '''Send notification to every distributor user about the warranty rejected'''

    warranty_data: dict = WarrantyPDF().dump(
        get_warranty_by_id_for_pdf(warranty_id))
    warranty_data = {
        **warranty_data,
        "date": datetime.now().strftime("%m/%d/%Y"),
        "distributor": warranty_data['distributor'],
        "reasons": warranty_data['reasons_names'],
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


def search_warranty_files(warranty_id: int, title: str, description: str, original_name: str, extension: str, page: int, per_page: int):
    '''Search warranties files'''

    query = [WarrantyFile.status == 'ACTIVE',
             WarrantyFile.warranty_id == warranty_id]
    if title:
        query.append(WarrantyFile.title.ilike(f'%{title}%'))
    if description:
        query.append(WarrantyFile.description.ilike(f'%{description}%'))
    if original_name:
        query.append(WarrantyFile.original_name.ilike(f'%{original_name}%'))
    if extension:
        query.append(WarrantyFile.extension.ilike(f'%{extension}%'))

    total = db.session.query(WarrantyFile)\
        .filter(*query)\
        .count()
    warranties_files = db.session.query(WarrantyFile)\
        .filter(*query)\
        .order_by(WarrantyFile.id.asc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    return warranties_files, total


def add_files(warranty_id: int, files: list[FileStorage]):
    '''Add warranty files'''

    for file in files:
        create_warranty_file(
            warranty_id=warranty_id,
            warranty_file_data=file,
        )
    db.session.commit()


def get_warranty_file(file_id: int):
    '''Get warranty file'''

    return db.session.query(WarrantyFile)\
        .filter(WarrantyFile.id == file_id)\
        .first()


def update_warranty_file(file_id: int, data: dict):
    '''Update warranty file'''

    db.session.merge(WarrantyFile(id=file_id, **data))
    db.session.commit()


def remove_warranty_file(warranty_file_id: int):
    '''Remove warranty file'''

    warranty_file = db.session.query(WarrantyFile)\
        .filter(
        WarrantyFile.id == warranty_file_id,
        WarrantyFile.status == 'ACTIVE'
    )\
        .first()
    try:
        Path(warranty_file.path).unlink(missing_ok=True)
    except Exception as e:
        print(
            f"Ocurrió un error al intentar eliminar el archivo: {e}")

    warranty_file.status = 'INACTIVE'
    db.session.merge(warranty_file)
    db.session.commit()
