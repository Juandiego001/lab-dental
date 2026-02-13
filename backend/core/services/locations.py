from core.app import db
from core.models import Country, State, City
from sqlalchemy import or_, and_


def search_countries(country_id: int, name: str, page: int, per_page: int):
    '''Search countries'''

    query = [Country.status == 'ACTIVE']
    with_id = None
    if name:
        query.append(Country.name.ilike(f'%{name}%'))
    if country_id:
        query.append(Country.id != country_id)
        with_id = db.session.query(Country)\
            .filter(Country.id == country_id).all()

    total = db.session.query(Country).filter(*query).count()
    total += len(with_id) if with_id else 0

    countries = db.session.query(Country)\
        .filter(*query)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_id:
        return countries, total
    return with_id + countries, total


def search_states(country_id: str, state_id: int, name: str, page: int, per_page: int):
    '''Search states'''

    query = [State.country_id == country_id, State.status == 'ACTIVE']
    with_id = None
    if name:
        query.append(State.name.ilike(f'%{name}%'))
    if state_id:
        query.append(State.id != state_id)
        with_id = db.session.query(State)\
            .filter(State.id == state_id).all()

    total = db.session.query(State).filter(*query).count()
    total += len(with_id) if with_id else 0

    states = db.session.query(State)\
        .filter(*query)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_id:
        return states, total
    return with_id + states, total


def search_cities(state_id: str, city_id: int, name: str, page: int, per_page: int):
    '''Search cities'''

    query = [City.state_id == state_id, City.status == 'ACTIVE']
    with_id = None
    if name:
        query.append(City.name.ilike(f'%{name}%'))
    if city_id:
        query.append(City.id != city_id)
        with_id = db.session.query(City)\
            .filter(City.id == city_id).all()

    total = db.session.query(City).filter(*query).count()
    total += len(with_id) if with_id else 0

    cities = db.session.query(City)\
        .filter(*query)\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()

    if not with_id:
        return cities, total
    return with_id + cities, total
