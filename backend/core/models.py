import enum
from core.app import db
from bcrypt import checkpw
from sqlalchemy import Column, Enum, Index, func, BigInteger, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression


class Country(db.Model):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')


class State(db.Model):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey('countries.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')


class City(db.Model):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state_id: Mapped[int] = mapped_column(
        ForeignKey('states.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20),
                                        nullable=False,
                                        server_default='ACTIVE')


class Address(db.Model):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey('countries.id'), nullable=False)
    state_id: Mapped[int] = mapped_column(
        ForeignKey('states.id'), nullable=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey('cities.id'), nullable=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
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


class Distributor(db.Model):
    __tablename__ = 'distributors'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
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


class Client(db.Model):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    distributor_id: Mapped[int] = mapped_column(
        ForeignKey('distributors.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
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
    email: Mapped[str] = mapped_column(String(450), nullable=True)
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


class Manual(db.Model):
    __tablename__ = 'manuals'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    manual_type_id: Mapped[int] = mapped_column(
        ForeignKey('manuals_types.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
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


class EquipmentFile(db.Model):
    __tablename__ = 'equipments_files'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey('equipments.id'), nullable=False)
    original_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_name: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    mimetype: Mapped[str] = mapped_column(String(100), nullable=False)
    extension: Mapped[str] = mapped_column(String(20), nullable=False)
    size: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default='0')
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

    equipment = relationship(
        'Equipment', primaryjoin='EquipmentFile.equipment_id == Equipment.id', backref='equipment_files')


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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
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


class Warranty(db.Model):
    __tablename__ = 'warranties'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    installation_id: Mapped[int] = mapped_column(
        ForeignKey('installations.id'), nullable=False)
    reasons_id: Mapped[int] = mapped_column(
        ForeignKey('reasons.id'), nullable=False)
    invoice: Mapped[str] = mapped_column(String(40), nullable=False)
    problem: Mapped[str] = mapped_column(String(400), nullable=False)
    solution: Mapped[str] = mapped_column(String(400), nullable=False)
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
