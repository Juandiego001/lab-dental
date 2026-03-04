"""data

Revision ID: fef0b7333d17
Revises: 882786e7d0d9
Create Date: 2026-03-04 05:55:44.319370

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import Brand, City, Country, Distributor, List_, DistributorList, State, User, UserList, \
    Group, UserGroup, Module, Permission, Category, ManualType, Equipment
import json
import pandas as pd


# revision identifiers, used by Alembic.
revision = 'fef0b7333d17'
down_revision = '882786e7d0d9'
branch_labels = None
depends_on = None


def upgrade():
    '''Initial data'''

    # Countries, states and cities
    countries_file = open(
        './locations_data/america_countries.json', 'r', encoding='utf-8')
    states_file = open('./locations_data/america_states.json',
                       'r', encoding='utf-8')
    cities_file = open('./locations_data/america_cities.json',
                       'r', encoding='utf-8')

    countries_json = json.load(countries_file)
    states_json = json.load(states_file)
    cities_json = json.load(cities_file)

    countries_file.close()
    states_file.close()
    cities_file.close()

    countries = []
    for country in countries_json:
        countries.append(Country(
            id=country['id'], code=country['iso3'], name=country['name'], status='ACTIVE'))
    db.session.add_all(countries)
    db.session.flush()

    states = []
    for state in states_json:
        states.append(State(
            id=state['id'], country_id=state['country_id'], name=state['name'], status='ACTIVE'))
    db.session.add_all(states)
    db.session.flush()

    cities = []
    for city in cities_json:
        cities.append(City(
            id=city['id'], state_id=city['state_id'], name=city['name'], status='ACTIVE'))
    db.session.add_all(cities)
    db.session.flush()

    # Distributor
    distributor = Distributor(name='Snapon')
    db.session.add(distributor)

    # List
    list_ = List_(name='Admins', slug='admins', is_main=True)
    db.session.add(list_)
    db.session.flush()

    # Distributor list
    distributor_list = DistributorList(
        distributor_id=distributor.id, list_id=list_.id)
    db.session.add(distributor_list)

    # User
    user = User(full_name='Juan Diego Cobo Cabal',
                username='juan',
                email='juandiego14012003@gmail.com',
                language='es',
                password='$2b$12$X7dhm0Idj49oUtZvzyJxd.ddFa7rvfilqaW4dzbkz0qYqs16uVrAi',
                role='ADMIN')
    db.session.add(user)
    db.session.flush()

    # User list
    user_list = UserList(user_id=user.id, list_id=list_.id)
    db.session.add(user_list)

    # Group
    group = Group(name='Admins', distributor_id=distributor.id)
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
        Module(name='lists'),
        Module(name='categories'),
        Module(name='installations'),
        Module(name='equipments'),
        Module(name='warranties'),
        Module(name='distributors'),
        Module(name='clients'),
        Module(name='sites'),
        Module(name='manuals'),
        Module(name='brands'),
        Module(name='reasons'),
        Module(name='parts'),
    ]
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

    # Categories
    categories = [
        Category(name='TIRE CHANGERS', slug='tire-changers'),
        Category(name='BALANCERS', slug='balancers'),
        Category(name='AIR CONDITIONERS', slug='air-conditioners'),
        Category(name='LIFTS', slug='lifts'),
        Category(name='BRAKE SERVICE', slug='break-service'),
        Category(name='WHEEL ALIGNERS', slug='wheel-aligners'),
        Category(name='TESTING EQUIPMENT', slug='testing-equipment'),
        Category(name='COLLISION REPAIR', slug='collision-repair'),
        Category(name='DIAGNOSTICS', slug='diagnostics')
    ]
    db.session.add_all(categories)
    db.session.flush()

    # Equipments
    df = pd.read_csv('equipments_data/equipments_with_categories.csv')
    equipments = []
    for index, row in df.iterrows():
        equipments.append(
            Equipment(
                brand_id=row['brand_id'],
                category_id=row['category_id'],
                model=row['model'],
                reference=row['reference']
            ))
    db.session.add_all(equipments)

    # Manuals Types
    manuals_types = [
        ManualType(name='Installation manuals', slug='installation-manuals'),
        ManualType(name='Service manuals', slug='service-manuals'),
        ManualType(name='Parts manuals', slug='parts-manuals'),
        ManualType(name='Newsletters', slug='newsletters'),
    ]
    db.session.add_all(manuals_types)
    db.session.flush()

    db.session.commit()


def downgrade():
    pass
