from core.app import db
from core.models import Address, City, Client, Country, Distributor, Site, State, User
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException
from sqlalchemy import func

from core.services.distributors import get_distributor_from_user


def get_sites(current_user: User, search: str, page: int, per_page: int):
    '''Get sites and total of sites in DB'''

    query = Site.status == 'ACTIVE'
    if search:
        query = and_(Site.status == 'ACTIVE',
                     or_(Site.name.ilike(f'%{search}%')))

    if current_user.role == 'ADMIN':
        total = db.session.query(Site).count()
        return list(db.session.execute(
            db.session.query(
                *Site.__table__.c,
                Client.name.label('client_name'),
                Distributor.name.label('distributor_name'))
            .outerjoin(Site.client)
            .outerjoin(Site.distributor)
            .filter(query)
            .order_by(Site.id.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        ).unique()), total

    distributor: Distributor = get_distributor_from_user(current_user)
    query = and_(query, or_(Site.distributor_id == distributor.id,
                 Client.distributor_id == distributor.id))
    total = db.session.query(Site)\
        .outerjoin(Site.client)\
        .outerjoin(Site.distributor)\
        .filter(query).count()
    return list(db.session.execute(
        db.session.query(
            *Site.__table__.c,
            Client.name.label('client_name'),
            Distributor.name.label('distributor_name'))
        .outerjoin(Site.client)
        .outerjoin(Site.distributor)
        .filter(query)
        .order_by(Site.id.desc())
        .limit(per_page)
        .offset((page - 1) * per_page)
    ).unique()), total


def get_clients_sites(client_id: int, search: str):
    '''Get clients sites'''

    query = and_(Site.status == 'ACTIVE', Site.client_id ==
                 client_id, Site.name.ilike(f'%{search}%'))
    return db.session.query(Site)\
        .filter(query)\
        .order_by(Site.id)


def get_distributors_sites(distributor_id: int, search: str):
    '''Get distributors sites'''

    query = and_(Site.status == 'ACTIVE', Site.distributor_id ==
                 distributor_id, Site.name.ilike(f'%{search}%'))
    return db.session.query(Site)\
        .filter(query)\
        .order_by(Site.id)


def get_site_by_id(site_id: int):
    '''Get site by site id'''

    return db.session.query(
        *Site.__table__.c,
        Address.id.label('address_id'),
        Address.description.label('description'),
        City.id.label('city_id'),
        City.name.label('city_name'),
        State.id.label('state_id'),
        State.name.label('state_name'),
        Country.id.label('country_id'),
        Country.name.label('country_name'),
        Client.name.label('client_name'),
        Distributor.name.label('distributor_name')
    )\
        .select_from(Site)\
        .join(Address)\
        .outerjoin(City, Address.city_id == City.id)\
        .outerjoin(State, Address.state_id == State.id)\
        .join(Country, Address.country_id == Country.id)\
        .outerjoin(Site.client)\
        .outerjoin(Site.distributor)\
        .filter(Site.id == site_id)\
        .first()


def create_site(current_user: User, site_model: Site, address_model: Address):
    '''
    Create Site

    :param current_user: Description
    :type current_user: User
    :param site_model: Description
    :type site_model: Site
    '''

    if not site_model.client_id and not (site_model.distributor_id):
        distributor: Distributor = get_distributor_from_user(current_user)
        site_model.distributor_id = distributor.id

    # Se crea objeto de dirección
    db.session.add(address_model)
    db.session.flush()

    # Se crea objeto de sede
    site_model.address_id = address_model.id
    db.session.add(site_model)
    db.session.commit()


def check_site_exists(site_id: int):
    '''Check if site exists'''

    return db.session.query(Site).filter(Site.id == site_id).first()


def update_site(site_id: int, site_load):
    '''Update site'''

    if not check_site_exists(site_id):
        raise HTTPException('Site not found')

    db.session.merge(site_load)
    db.session.commit()


def delete_site(site_id: int):
    '''Delete site'''

    db.session.merge(Site(id=site_id, status='INACTIVE'))
    db.session.commit()
