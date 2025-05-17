"""Initial data

Revision ID: ddeb77e2f92b
Revises: 9c773e01122a
Create Date: 2025-05-10 12:39:12.404982

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import Brand, City, Country, Distributor, List_, DistributorList, State, User, UserList, Group, UserGroup, Module, Permission
import json


# revision identifiers, used by Alembic.
revision = 'ddeb77e2f92b'
down_revision = '9c773e01122a'
branch_labels = None
depends_on = None


def upgrade():
    '''Initial data'''

    # Countries, states and cities
    countries_file = open('./locations_data/america_countries.json', 'r', encoding='utf-8')
    states_file = open('./locations_data/america_states.json', 'r', encoding='utf-8')
    cities_file = open('./locations_data/america_cities.json', 'r', encoding='utf-8')

    countries_json = json.load(countries_file)
    states_json = json.load(states_file)
    cities_json = json.load(cities_file)

    countries_file.close()
    states_file.close()
    cities_file.close()

    countries = []
    for country in countries_json:
        countries.append(Country(id=country['id'], code=country['iso3'], name=country['name'], status='ACTIVE'))
    db.session.add_all(countries)
    db.session.flush()

    states = []
    for state in states_json:
        states.append(State(id=state['id'], country_id=state['country_id'], name=state['name'], status='ACTIVE'))
    db.session.add_all(states)
    db.session.flush()

    cities = []
    for city in cities_json:
        cities.append(City(id=city['id'], state_id=city['state_id'], name=city['name'], status='ACTIVE'))
    db.session.add_all(cities)
    db.session.flush()

    # Distributor
    distributor = Distributor(name='Snapon')
    db.session.add(distributor)

    # List
    list_ = List_(name='Admins', slug='admins')
    db.session.add(list_)
    db.session.flush()

    # Distributor list
    distributor_list = DistributorList(distributor_id=distributor.id, list_id=list_.id)
    db.session.add(distributor_list)

    # User
    user = User(full_name='Juan Diego Cobo Cabal',
                username='juan',
                email='juandiego14012003@gmail.com',
                password='$2b$12$X7dhm0Idj49oUtZvzyJxd.ddFa7rvfilqaW4dzbkz0qYqs16uVrAi',
                type='ADMIN')
    db.session.add(user)
    db.session.flush()

    # User list
    user_list = UserList(user_id=user.id, list_id=list_.id)
    db.session.add(user_list)

    # Group
    group = Group(name='Admins')
    db.session.add(group)
    db.session.flush()

    # User Group
    user_group = UserGroup(user_id=user.id, group_id=group.id)
    db.session.add(user_group)

    # Modules
    modules = [
        Module(name='users'),
        Module(name='groups'),
        Module(name='forums'),
        Module(name='strapi'),
        Module(name='zones'),
        Module(name='categories'),
        Module(name='installations'),
        Module(name='equipments'),
        Module(name='warranties'),
        Module(name='distributors'),
        Module(name='manuals'),
        Module(name='brands')]
    db.session.add_all(modules)
    db.session.flush()

    # Permissions
    permissions = []
    for module in modules:
        permission = Permission(
            group_id=group.id,
            module_id=module.id,
            read=True,
            create=True,
            update=True,
            delete=True)
        permissions.append(permission)
    db.session.add_all(permissions)
    db.session.flush()

    # Brands
    brands = [
        Brand(name='Total Shop Solutions (TSS)', slug='total-shop-solutions'),
        Brand(name='Sun', slug='sun'),
        Brand(name='John Bean', slug='john-bean'),
        Brand(name='Mitchell1', slug='mitchell1'),
        Brand(name='Black Hawk', slug='black-hawk'),
        Brand(name='Hofmann', slug='hofmann'),
        Brand(name='Kansas Jack', slug='kansas-jack'),
        Brand(name='Boxer', slug='boxer'),
        Brand(name='Cartec', slug='cartec'),
        Brand(name='Challenger Lifts', slug='challenger-lifts'),
        Brand(name='Pro-Cut', slug='pro-cut'),
        Brand(name='Ecotechnics', slug='ecotechnics'),
        Brand(name='Car-o-liner', slug='car-o-liner'),
        Brand(name='Josam', slug='josam'),
        Brand(name='Truck Cam', slug='truck-cam'),
        Brand(name='Snap On', slug='snap-on'),
    ]
    db.session.add_all(brands)
    db.session.flush()
    db.session.flush()

    db.session.commit()

def downgrade():
    pass
