"""Add Aligners modules

Revision ID: 83cb3b31ab06
Revises: ad80b2ef1df3
Create Date: 2026-07-31 12:44:10.495370

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import Group, Module, Permission


# revision identifiers, used by Alembic.
revision = '83cb3b31ab06'
down_revision = 'ad80b2ef1df3'
branch_labels = None
depends_on = None


def upgrade():
    '''Add aligners modules'''

    module = Module(name='aligners')
    db.session.add(module)
    db.session.flush()

    # Se crea el permiso para el grupo de administradores
    permission = Permission(
        group_id=1,
        module_id=module.id,
        read=True,
        create=True,
        update=True,
        delete=True)
    db.session.add(permission)

    # Se crea el permiso para todos los demás grupos diferentes del grupo de administradores en False
    groups = db.session.query(Group).filter(Group.id != 1).all()
    permissions_groups = []
    for group in groups:
        permission_group = Permission(
            group_id=group.id,
            module_id=module.id,
            read=False,
            create=False,
            update=False,
            delete=False)
        permissions_groups.append(permission_group)

    db.session.add_all(permissions_groups)
    db.session.commit()


def downgrade():
    pass
