import re
import math
from flask import json
import requests
import unicodedata
from core.app import db
from flask_babel import gettext
from core.models import Client, Contact, Distributor, DistributorAligner, DistributorBrand, DistributorEmail, DistributorList, DistributorPhone, List_, User, UserList
from sqlalchemy import delete, func, and_, select
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from datetime import datetime, date


def search_distributors(current_user: User, distributors_ids: list[int], name: str, bp: str, page: int, per_page: int, sort_by: dict = None):
    '''Search distributors'''

    order_by = Distributor.id.desc()
    if sort_by and isinstance(sort_by, dict):
        sort_key = sort_by.get('key')
        sort_order = sort_by.get('order', 'asc')
        if sort_key and hasattr(Distributor, sort_key):
            column = getattr(Distributor, sort_key)
            if sort_order == 'desc':
                order_by = column.desc()
            else:
                order_by = column.asc()

    query = [Distributor.status == 'ACTIVE']
    with_distributors_ids = None
    if name:
        query.append(Distributor.name.ilike(f'%{name}%'))
    if bp:
        query.append(Distributor.bp.ilike(f'%{bp}%'))
    if distributors_ids:
        query.append(Distributor.id.not_in(distributors_ids))
        with_distributors_ids = db.session.query(Distributor)\
            .filter(Distributor.id.in_(distributors_ids))\
            .all()

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(Distributor.id == distributor.id)

    total = db.session.query(Distributor)\
        .filter(*query).count()
    total += len(with_distributors_ids) if with_distributors_ids else 0

    distributors = db.session.query(Distributor)\
        .options(
            joinedload(Distributor.distributors_brands)
    )\
        .filter(*query)\
        .group_by(Distributor.id, Distributor.name)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_distributors_ids:
        return distributors, total
    return with_distributors_ids + distributors, total


def get_clients_by_distributor_id(distributor_id: int, search: str):
    '''Get clients by distributor id'''

    query = [and_(Distributor.id == distributor_id, Client.status == 'ACTIVE')]
    if search:
        query.append(Client.name.ilike(f'%{search}%'))

    return db.paginate(db.session.query(Client)
                       .join(Distributor)
                       .filter(*query),
                       page=1, per_page=15)


def get_distributor_from_user(user: User) -> Distributor:
    '''Get distributor from user'''

    return db.session.query(Distributor)\
        .select_from(Distributor)\
        .join(DistributorList)\
        .join(List_)\
        .join(UserList)\
        .join(User)\
        .filter(and_(User.id == user.id, List_.is_main))\
        .first()


def get_distributor_by_id(distributor_id: int):
    '''Get distributor by distributor id'''

    return db.session.query(Distributor)\
        .options(
            joinedload(Distributor.distributors_emails.and_(
                DistributorEmail.status == 'ACTIVE'
            )),
            joinedload(Distributor.distributors_phones.and_(
                DistributorPhone.status == 'ACTIVE'
            )),
            joinedload(Distributor.distributors_brands)
    )\
        .filter(Distributor.id == distributor_id)\
        .group_by(Distributor.id)\
        .first()


def check_distributor_exists(distributor_id: int):
    '''Check if distributor exists'''

    return db.session.query(Distributor).filter(Distributor.id == distributor_id).first()


def save_distributor_emails(distributor_id: int, emails: list[str]):
    '''Save distributor emails'''

    for email_dict in emails:
        if 'id' in email_dict:
            db.session.merge(DistributorEmail(**email_dict))
        else:
            db.session.add(DistributorEmail(
                distributor_id=distributor_id,
                email=email_dict['email']
            ))

    db.session.commit()


def save_distributor_phones(distributor_id: int, phones: list[str]):
    '''Save distributor phones'''

    for phone_dict in phones:
        if 'id' in phone_dict:
            db.session.merge(DistributorPhone(**phone_dict))
        else:
            db.session.add(DistributorPhone(
                distributor_id=distributor_id,
                phone=phone_dict['phone']
            ))

    db.session.commit()


def save_distributors_brands(distributor_id: int, brands_ids: list[int]):
    '''Save distributors brands'''

    # Se remueven los distributors_brands creados previamente
    db.session.execute(delete(DistributorBrand).where(
        DistributorBrand.distributor_id == distributor_id))

    # Se crean los nuevos distributors_brands
    distributors_brands = [
        DistributorBrand(distributor_id=distributor_id, brand_id=brand_id)
        for brand_id in brands_ids
    ]
    db.session.add_all(distributors_brands)

    db.session.commit()


def create_distributor(data: dict):
    '''Create distributor'''

    brands_ids = data.pop('brands_ids')
    emails = data.pop('emails')
    phones = data.pop('phones')
    name = data['name']

    new_distributor = Distributor(**data)
    db.session.add(new_distributor)

    # Slug generation process
    slug = f'Main {name}'.lower()
    slug = unicodedata.normalize('NFKD', slug).encode(
        'ascii', 'ignore').decode('utf-8')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')

    list_ = List_(name=f'Main {name}', slug=slug, is_main=True)
    db.session.add(list_)
    db.session.flush()

    distributor_list = DistributorList(
        distributor_id=new_distributor.id, list_id=list_.id)
    db.session.add(distributor_list)
    db.session.commit()

    if brands_ids:
        save_distributors_brands(
            distributor_id=new_distributor.id,
            brands_ids=brands_ids
        )

    if emails and len(emails):
        save_distributor_emails(
            distributor_id=new_distributor.id,
            emails=emails
        )

    if phones and len(phones):
        save_distributor_phones(
            distributor_id=new_distributor.id,
            phones=phones
        )


def update_distributor(distributor_id: int, data: dict):
    '''Update distributor'''

    if not check_distributor_exists(distributor_id):
        raise HTTPException('Distributor not found')

    brands_ids = data.pop('brands_ids')
    emails = data.pop('emails')
    phones = data.pop('phones')
    db.session.merge(Distributor(**data))
    db.session.commit()

    save_distributors_brands(
        distributor_id=distributor_id,
        brands_ids=brands_ids
    )

    if emails and len(emails):
        save_distributor_emails(
            distributor_id=distributor_id,
            emails=emails
        )

    if phones and len(phones):
        save_distributor_phones(
            distributor_id=distributor_id,
            phones=phones
        )


def delete_distributor(distributor_id: int):
    '''Delete distributor'''

    distributor_list_subquery = db.session.query(DistributorList.list_id).filter(
        DistributorList.distributor_id == distributor_id).subquery()

    lists_ = db.session.query(
        List_.id.label('list_id'),
        func.array_agg(DistributorList.distributor_id).label('distributors')
    )\
        .select_from(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(Distributor.status == 'ACTIVE', List_.id.in_(select(distributor_list_subquery)))\
        .group_by(List_.id)\
        .all()

    unique_lists = [each_list.list_id for each_list in lists_ if len(
        each_list.distributors) == 1]
    for list_id in unique_lists:
        db.session.merge(List_(id=list_id, status='INACTIVE'))

    db.session.merge(Distributor(id=distributor_id, status='INACTIVE'))
    db.session.commit()


def search_contacts(distributor_id: int, contacts_ids: list[int], full_name: str, email: str, phone: str, page: int, per_page: int, sort_by: dict = None):
    '''Search contacts'''

    order_by = Contact.id.desc()
    if sort_by:
        if sort_by['key'] == 'fullName':
            order_by = Contact.full_name
        elif sort_by['key'] == 'email':
            order_by = Contact.email
        elif sort_by['key'] == 'phone':
            order_by = Contact.phone
        order_by = order_by.asc(
        ) if sort_by['order'] == 'asc' else order_by.desc()

    query = [Contact.status == 'ACTIVE',
             Contact.distributor_id == distributor_id]
    with_contacts_ids = None
    if full_name:
        query.append(Contact.full_name.ilike(f'%{full_name}%'))
    if email:
        query.append(Contact.email.ilike(f'%{email}%'))
    if phone:
        query.append(Contact.phone.ilike(f'%{phone}%'))
    if contacts_ids:
        query.append(Contact.id.not_in(contacts_ids))
        with_contacts_ids = db.session.query(Contact)\
            .filter(Contact.id.in_(contacts_ids))\
            .all()

    total = db.session.query(Contact)\
        .filter(*query).count()
    total += len(with_contacts_ids) if with_contacts_ids else 0

    contacts = db.session.query(Contact)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_contacts_ids:
        return contacts, total
    return with_contacts_ids + contacts, total


def create_contacts(data: dict):
    '''Create contacts'''

    db.session.add(Contact(**data))
    db.session.commit()


def get_contact_by_email(email: str):
    '''Get contact by email'''

    return db.session.query(Contact)\
        .filter(Contact.email == email, Contact.status == 'ACTIVE')\
        .first()


def update_contacts(contact_id: int, data: dict):
    '''Update contacts'''

    the_contact = get_contact_by_id(contact_id=contact_id)
    if not the_contact:
        raise HTTPException(gettext('contactNotFound'))

    if 'email' in data and (data['email'] != the_contact.email) and get_contact_by_email(email=data['email']):
        raise HTTPException(gettext('contactEmailExistsError'))

    db.session.merge(Contact(**data))
    db.session.commit()


def get_contact_by_id(contact_id: int):
    '''Get contact by ID'''

    return db.session.query(Contact)\
        .filter(Contact.id == contact_id)\
        .first()


def delete_contact_by_id(contact_id: int):
    '''Delete contact by ID'''

    db.session.merge(Contact(id=contact_id, status='INACTIVE'))
    db.session.commit()


def get_aliners_info_with_connection(serials: list[tuple[str, str]]) -> list[dict]:
    '''Get aligners info from vehicles with connection'''

    data = []
    for (id, serial) in serials:
        response = requests.get(
            'https://vehicle365.org/read/aligner/v1/',
            params={
                'serialNumber': serial,
                'username': 'andresleon',
            }
        )
        if response.status_code != 200:
            continue

        info = response.json()
        if not 'specs' in info:
            continue
        data.append({
            **info,
            'id': id,
        })
    return data


def get_aliners_info(serials: list[str] | set[str]) -> list[dict]:
    '''Get aligners info from vehicles'''

    total_pages = math.ceil(len(serials)/10)
    data = []
    for page in range(total_pages):
        since = 10*page
        filter_serials = '|'.join(list(serials)[since:since+10])
        response = requests.get(
            f'https://vehicle365.org/read/aligners/v1/?page=1&filterSerialNumber={filter_serials}'
        )
        if response.status_code != 200:

            continue

        data += response.json()['docs']

    return data


def aligner_exist(serial: str) -> bool | dict:
    '''Verify if aligner exist by given serial'''

    try:
        response = requests.get(
            f'https://vehicle365.org/read/aligner/v1/?serialNumber={serial}&username=andresleon')
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        return False


def associate_aligner_to_distributor(serial: str, distributor_id: int):
    '''Associate aligner to distributor'''

    aligner_data = get_aliners_info(serials=[serial])[0]
    specs = aligner_data['specs']
    db.session.add(DistributorAligner(
        serial=serial,
        specs=f'{specs['name']} {specs['month']}/{specs['year']}',
        software=aligner_data['version']['semantic'],
        v_created_at=aligner_data['createdAt'],
        distributor_id=distributor_id
    ))
    db.session.commit()


def validate_aligners_file(distributor_id: int, file: FileStorage):
    '''Validate aligners file'''

    validations = []
    file_content: list[str] = file\
        .read()\
        .decode('utf-8')\
        .splitlines()

    serials = set([line.strip().upper() for line in file_content])
    existing_serials = db.session.scalars(
        db.session.query(DistributorAligner.serial)
        .filter(DistributorAligner.serial.in_(serials)
                ))

    for serial in existing_serials:
        validations.append({
            'serial': serial,
            'message_type': 'warning',
            'message': gettext('alignerAlreadyAssociated')
        })
        serials.remove(serial)

    data = get_aliners_info(serials=serials)
    the_serials = [aligner['serialNumber'] for aligner in data]
    the_specs = {aligner["serialNumber"]: aligner.get(
        "specs", None) for aligner in data}

    for serial in serials:
        if serial not in the_serials:
            validations.append({
                'serial': serial,
                'message_type': 'error',
                'message': gettext('alignerNotFound')
            })
        elif not the_specs[serial]:
            validations.append({
                'serial': serial,
                'message_type': 'error',
                'message': gettext('alignerSpecsNotFound')
            })
        else:
            validations.append({
                'serial': serial,
                'message_type': 'success',
                'message': gettext('alignerCanBePaired')
            })

    return validations


def upload_multiple_aligners(distributor_id: int, serials: list[dict]):
    '''Upload multiple aligners after the text validation'''

    serials = [serial['serial'] for serial in serials]
    existing_serials = db.session.query(DistributorAligner.serial)\
        .filter(
        and_(
            DistributorAligner.distributor_id == distributor_id,
            DistributorAligner.serial.in_(serials)
        )
    ).all()

    if existing_serials:
        raise HTTPException(gettext('someAlignersAreAlreadyAssociated'))

    data = get_aliners_info(serials=serials)
    data_serials = [aligner['serialNumber'] for aligner in data]
    for serial in serials:
        if serial not in data_serials:
            raise HTTPException(gettext('someAlignersDoesNotExist'))

    for aligner_data in data:
        db.session.add(
            DistributorAligner(
                distributor_id=distributor_id,
                serial=aligner_data['serialNumber']
            ))

    db.session.commit()


def unlink_distributor_aligner(aligner_id: int):
    '''Unlink distributor aligner'''

    db.session.execute(delete(DistributorAligner).where(
        DistributorAligner.id == aligner_id))
    db.session.commit()


def get_all_aligners(distributor_id: int):
    '''Get all aligners of a distributor'''

    aligners = db.session.query(DistributorAligner.id, DistributorAligner.serial)\
        .filter(DistributorAligner.distributor_id == distributor_id)\
        .all()

    results = get_aliners_info_with_connection(
        serials=[(aligner.id, aligner.serial) for aligner in aligners])
    return {'items': results}


def stream_all_aligners(distributor_id: int):
    '''Yield aligners of a distributor one by one as Server-Sent Events'''

    aligners = db.session.query(DistributorAligner.id, DistributorAligner.alias, DistributorAligner.serial)\
        .filter(DistributorAligner.distributor_id == distributor_id)\
        .order_by(DistributorAligner.id.desc())\
        .all()

    for (id, alias, serial) in aligners:
        response = requests.get(
            'https://vehicle365.org/read/aligner/v1/',
            params={
                'serialNumber': serial,
                'username': 'andresleon',
            }
        )

        if response.status_code == 200:
            info = response.json()
            if not 'specs' in info:
                info['specs'] = None

            data_item = {
                **info,
                'id': id,
                'alias': alias
            }
            # Formato SSE estándar: "data: {json}\n\n"
            yield f"data: {json.dumps(data_item)}\n\n"


def set_aligner_alias(current_user: User, aligner_id: int, alias: str):
    '''Set aligner alias'''

    filters_ = [DistributorAligner.id == aligner_id]
    distributor_id = get_distributor_from_user(user=current_user).id
    if distributor_id != 1:
        filters_.append(DistributorAligner.distributor_id == distributor_id)

    the_aligner = db.session.query(DistributorAligner)\
        .filter(and_(*filters_)).first()

    if not the_aligner:
        raise HTTPException(gettext('alignerNotFound'))

    the_aligner.alias = alias
    db.session.commit()
