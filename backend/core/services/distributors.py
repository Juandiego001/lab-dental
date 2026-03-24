import re
import unicodedata
from core.app import db
from flask_babel import gettext
from core.models import Client, Contact, Distributor, DistributorEmail, DistributorList, DistributorPhone, List_, User, UserList
from sqlalchemy import func, and_, select
from sqlalchemy.orm import joinedload
from http.client import HTTPException


def search_distributors(current_user: User, distributors_ids: list[int], name: str, page: int, per_page: int, sort_by: dict = None):
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
        .filter(*query)\
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
            ))
    )\
        .filter(Distributor.id == distributor_id)\
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


def create_distributor(data: dict):
    '''Create distributor'''

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

    emails = data.pop('emails')
    phones = data.pop('phones')
    db.session.merge(Distributor(**data))
    db.session.commit()

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


def search_contacts(distributor_id: int, full_name: str, email: str, phone: str, page: int, per_page: int, sort_by: dict = None):
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
    if full_name:
        query.append(Contact.full_name.ilike(f'%{full_name}%'))
    if email:
        query.append(Contact.email.ilike(f'%{email}%'))
    if phone:
        query.append(Contact.phone.ilike(f'%{phone}%'))

    total = db.session.query(Contact)\
        .filter(*query).count()
    contacts = db.session.query(Contact)\
        .filter(*query)\
        .order_by(order_by)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    return contacts, total


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
