from core.app import db
from core.models import Country, State, City
from sqlalchemy import or_, and_
from werkzeug.exceptions import HTTPException


def get_countries(search: str, page: int, per_page: int):
    '''Get countries'''

    query = Country.status == 'ACTIVE'
    if search:
        query = and_(Country.status == 'ACTIVE',
                     or_(Country.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(Country).filter(query),
                       page=page, per_page=per_page)


def get_states(country_id: str, search: str, page: int, per_page: int):
    '''Get states'''

    query = and_(State.country_id == country_id, State.status == 'ACTIVE')
    if search:
        query = and_(
            State.country_id == country_id,
            State.status == 'ACTIVE',
            or_(State.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(State).filter(query),
                       page=page, per_page=per_page)


def get_cities(state_id: str, search: str, page: int, per_page: int):
    '''Get cities'''

    query = and_(City.state_id == state_id, City.status == 'ACTIVE')
    if search:
        query = and_(
                    City.state_id == state_id,
                    City.status == 'ACTIVE',
                     or_(City.name.ilike(f'%{search}%')))

    return db.paginate(db.session.query(City).filter(query),
                       page=page, per_page=per_page)
