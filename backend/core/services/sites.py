from core.app import db
from core.models import Address, City, Client, Country, Distributor, Site, State
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException
from sqlalchemy import func


def get_sites(search: str, page: int, per_page: int):
    '''Get sites and total of sites in DB'''

    query = Site.status == 'ACTIVE'
    if search:
        query = and_(Site.status == 'ACTIVE',
                     or_(Site.name.ilike(f'%{search}%')))

    total = db.session.query(Site).count()

    return list(db.session.execute(
        db.session.query(
            *Site.__table__.c,
            func.concat(
                Client.name, Distributor.name).label('distributor_client'))
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
        Address.city_id.label('city_id'),
        City.state_id.label('state_id'),
        City.name.label('city_name'),
        State.country_id.label('country_id'),
        State.name.label('state_name'),
        Country.name.label('country_name'),
    )\
        .select_from(Site)\
        .join(Address)\
        .join(City)\
        .join(State)\
        .join(Country)\
        .filter(Site.id == site_id)\
        .first()


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
