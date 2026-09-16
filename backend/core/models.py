import enum
from core.app import db
from bcrypt import checkpw
from sqlalchemy import UniqueConstraint, Column, Enum, Index, Integer, Text, func, BigInteger, String, DateTime, ForeignKey, Boolean, text
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import JSONB


class Country(db.Model):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    address = relationship('Address', back_populates='country')


class State(db.Model):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey('countries.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    address = relationship('Address', back_populates='state')


class City(db.Model):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state_id: Mapped[int] = mapped_column(
        ForeignKey('states.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    address = relationship('Address', back_populates='city')


class Address(db.Model):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey('countries.id'), nullable=False)
    state_id: Mapped[int] = mapped_column(
        ForeignKey('states.id'), nullable=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey('cities.id'), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(40), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    site = relationship(
        'Site', back_populates='address')
    city = relationship(
        'City', back_populates='address')
    state = relationship(
        'State', back_populates='address')
    country = relationship(
        'Country', back_populates='address')


class Distributor(db.Model):
    __tablename__ = 'distributors'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    bp: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    notes: Mapped[str] = mapped_column(String(), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    client = relationship('Client', back_populates='distributor')
    site = relationship('Site', back_populates='distributor')
    distributors_brands = relationship(
        'DistributorBrand', back_populates='distributor')
    distributors_emails = relationship(
        'DistributorEmail', back_populates='distributor')
    distributors_phones = relationship(
        'DistributorPhone', back_populates='distributor')
    contacts = relationship(
        'Contact', back_populates='distributor')
    distributors_aligners = relationship(
        'DistributorAligner', back_populates='distributor')


class DistributorBrand(db.Model):
    __tablename__ = 'distributors_brands'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    brand_id: Mapped[int] = mapped_column(
        ForeignKey('brands.id'), nullable=False)

    distributor = relationship(
        'Distributor', back_populates='distributors_brands')
    brand = relationship(
        'Brand', back_populates='distributors_brands')


class DistributorEmail(db.Model):
    __tablename__ = 'distributors_emails'
    __table_args__ = (
        Index(
            'unique_email_status_distributor_email',  # Index name
            'email', 'status',  # Columns which are part of the index
            unique=True,
            postgresql_where=Column('status') == 'ACTIVE'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    email: Mapped[str] = mapped_column(
        String(450), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    distributor = relationship(
        'Distributor', back_populates='distributors_emails')


class DistributorPhone(db.Model):
    __tablename__ = 'distributors_phones'
    __table_args__ = (
        Index(
            'unique_phone_status',  # Index name
            'phone', 'status',  # Columns which are part of the index
            unique=True,
            postgresql_where=Column('status') == 'ACTIVE'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    phone: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    distributor = relationship(
        'Distributor', back_populates='distributors_phones')


class DistributorAligner(db.Model):
    __tablename__ = 'distributors_aligners'
    __table_args__ = (
        Index(
            'unique_serial_status',  # Index name
            'serial', 'status',  # Columns which are part of the index
            unique=True,
            postgresql_where=Column('status') == 'ACTIVE'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    serial: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    alias: Mapped[str] = mapped_column(
        String(100), nullable=True, comment='Aligner Alias')
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        comment='Created at registered in the SOE DB. Different from v_created_at.')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    distributor = relationship(
        'Distributor', back_populates='distributors_aligners')


class Contact(db.Model):
    __tablename__ = 'contacts'
    __table_args__ = (
        Index(
            'unique_email_status_contact',  # Index name
            'email', 'status',  # Columns which are part of the index
            unique=True,
            postgresql_where=Column('status') == 'ACTIVE'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[str] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String(450), nullable=True)
    phone: Mapped[str] = mapped_column(
        String(100), nullable=True)
    notes: Mapped[str] = mapped_column(String(), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    distributor = relationship(
        'Distributor', back_populates='contacts')


class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = (
        Index(
            'uq_active_distributor_client_name',
            'distributor_id',
            'name',
            unique=True,
            postgresql_where=text("status = 'ACTIVE'")
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    distributor = relationship('Distributor', back_populates='client')
    site = relationship('Site', back_populates='client')


class Site(db.Model):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'), nullable=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=True)
    address_id: Mapped[int] = mapped_column(
        ForeignKey('addresses.id'), nullable=False)

    is_main: Mapped[str] = mapped_column(
        Boolean, nullable=False, server_default=expression.false())

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    distributor = relationship('Distributor', back_populates='site')
    client = relationship('Client', back_populates='site')
    address = relationship('Address', back_populates='site')


class List_(db.Model):
    __tablename__ = 'lists'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    slug: Mapped[str] = mapped_column(String(60), nullable=False)
    is_main: Mapped[Boolean] = mapped_column(
        Boolean, nullable=False, server_default=expression.false())
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class DistributorList(db.Model):
    __tablename__ = 'distributors_lists'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    list_id: Mapped[int] = mapped_column(
        ForeignKey('lists.id'), nullable=False)


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            'unique_email_status',  # Index name
            'email', 'status',  # Columns which are part of the index
            unique=True,
            postgresql_where=Column('status') == 'ACTIVE'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(450), nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    language: Mapped[str] = mapped_column(
        String(10), nullable=False, server_default='es')
    photo_path: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    user_groups = relationship('UserGroup', back_populates='user')

    def check_password(self, password: str):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class UserList(db.Model):
    __tablename__ = 'users_lists'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    list_id: Mapped[int] = mapped_column(
        ForeignKey('lists.id'), nullable=False)


class Group(db.Model):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    user_groups = relationship('UserGroup', back_populates='group')


class UserGroup(db.Model):
    __tablename__ = 'user_groups'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    user = relationship('User', back_populates='user_groups')
    group = relationship('Group', back_populates='user_groups')


class Module(db.Model):
    __tablename__ = 'modules'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Permission(db.Model):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id'), nullable=False)
    module_id: Mapped[int] = mapped_column(
        ForeignKey('modules.id'), nullable=False)
    read: Mapped[bool] = mapped_column()
    create: Mapped[bool]
    update: Mapped[bool]
    delete: Mapped[bool]
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Brand(db.Model):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    equipment = relationship('Equipment', back_populates='brand')
    distributors_brands = relationship(
        'DistributorBrand', back_populates='brand')


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    equipment = relationship('Equipment', back_populates='category')


class Equipment(db.Model):
    __tablename__ = 'equipments'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    brand_id: Mapped[int] = mapped_column(
        ForeignKey('brands.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    reference: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())
    brand = relationship('Brand', back_populates='equipment')
    category = relationship('Category', back_populates='equipment')
    equipment_files = relationship('EquipmentFile', back_populates='equipment')


class ManualType(db.Model):
    __tablename__ = 'manuals_types'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    manual = relationship('Manual', back_populates='manual_type')


class Manual(db.Model):
    __tablename__ = 'manuals'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    manual_type_id: Mapped[int] = mapped_column(
        ForeignKey('manuals_types.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    manual_type = relationship(
        'ManualType', back_populates='manual', uselist=False)
    manual_file = relationship(
        'ManualFile', back_populates='manual', uselist=False)


class ManualFile(db.Model):
    __tablename__ = 'manuals_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    manual_id: Mapped[int] = mapped_column(
        ForeignKey('manuals.id'), nullable=False)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_name: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    mimetype: Mapped[str] = mapped_column(String(100), nullable=False)
    extension: Mapped[str] = mapped_column(String(20), nullable=False)
    size: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default='0')
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    manual = relationship('Manual', back_populates='manual_file')


class EquipmentFile(db.Model):
    __tablename__ = 'equipments_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_name: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    mimetype: Mapped[str] = mapped_column(String(100), nullable=False)
    extension: Mapped[str] = mapped_column(String(20), nullable=False)
    size: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default='0')
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default='0')
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())

    equipment = relationship('Equipment', back_populates='equipment_files')


class Part(db.Model):
    __tablename__ = 'parts'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    serial: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Specification(db.Model):
    __tablename__ = 'specifications'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    value: Mapped[str] = mapped_column(String(120), nullable=False)
    field_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Installation(db.Model):
    __tablename__ = 'installations'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    site_distributor_id: Mapped[int] = mapped_column(
        ForeignKey('sites.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'), nullable=False)
    site_client_id: Mapped[int] = mapped_column(
        ForeignKey('sites.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    serial: Mapped[str] = mapped_column(String(), nullable=False)
    installed_date: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Installation_File_Type(enum.Enum):
    FORMAT = 'FORMAT'
    SERIAL = 'SERIAL'
    EVIDENCES = 'EVIDENCES'


class InstallationFile(db.Model):
    __tablename__ = 'installations_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey('installations.id'), nullable=False)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_name: Mapped[str] = mapped_column(String(100), nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    mimetype: Mapped[str] = mapped_column(String(100), nullable=True)
    extension: Mapped[str] = mapped_column(String(20), nullable=True)
    size: Mapped[int] = mapped_column(
        BigInteger, nullable=True, server_default='0')
    file_type: Mapped[str] = mapped_column(Enum(Installation_File_Type), nullable=False,
                                           comment='Installation file type could be one of [FORMAT, SERIAL, EVIDENCES]')
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Reason(db.Model):
    __tablename__ = 'reasons'
    __table_args__ = (
        Index(
            'uq_active_reason_category_slug',
            'category_id',
            'slug',
            unique=True,
            postgresql_where=text("status = 'ACTIVE'")
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class WarrantyFile(db.Model):
    __tablename__ = 'warranties_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warranty_id: Mapped[int] = mapped_column(
        ForeignKey('warranties.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_name: Mapped[str] = mapped_column(String(100), nullable=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    mimetype: Mapped[str] = mapped_column(String(100), nullable=True)
    extension: Mapped[str] = mapped_column(String(20), nullable=True)
    size: Mapped[int] = mapped_column(
        BigInteger, nullable=True, server_default='0')
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class Warranty(db.Model):
    __tablename__ = 'warranties'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    site_id: Mapped[int] = mapped_column(
        ForeignKey('sites.id'), nullable=False)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    contact_id: Mapped[int] = mapped_column(
        ForeignKey('contacts.id'), nullable=False)
    user_approval_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey('installations.id'), nullable=True)

    sale_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    invoice: Mapped[str] = mapped_column(String(40), nullable=False)
    serial: Mapped[str] = mapped_column(String(100), nullable=True)
    shipt_to: Mapped[str] = mapped_column(String(400), nullable=False)
    problem: Mapped[str] = mapped_column(String(400), nullable=False)
    solution: Mapped[str] = mapped_column(String(400), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    parts: Mapped[dict] = mapped_column(JSONB, nullable=True)

    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now())


class WarrantyReason(db.Model):
    __tablename__ = 'warranties_reasons'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warranty_id: Mapped[int] = mapped_column(
        ForeignKey('warranties.id'), nullable=False)
    reason_id: Mapped[int] = mapped_column(
        ForeignKey('reasons.id'), nullable=False)


class WarrantyWCO(db.Model):
    __tablename__ = 'warranties_wcos'
    __table_args__ = (
        UniqueConstraint('code', 'year', name='uq_warranty_wco_code_year'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warranty_id: Mapped[int] = mapped_column(
        ForeignKey('warranties.id'), nullable=False)
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
