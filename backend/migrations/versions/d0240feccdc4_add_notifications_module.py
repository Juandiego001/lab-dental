"""Add notifications module

Revision ID: d0240feccdc4
Revises: fd4cabb69465
Create Date: 2026-09-28 13:23:46.809176

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import Group, Module, Permission


# revision identifiers, used by Alembic.
revision = 'd0240feccdc4'
down_revision = 'fd4cabb69465'
branch_labels = None
depends_on = None


def upgrade():
    '''Add notifications module'''

    new_module = Module(name='notifications', status='ACTIVE')
    db.session.add(new_module)
    db.session.flush()

    groups = db.session.query(Group).all()
    the_permissions = []
    for group in groups:
        if group.id != 1:
            the_permissions.append(Permission(group_id=group.id, module_id=new_module.id,
                                              read=False, create=False, update=False, delete=False))
            continue
        else:
            the_permissions.append(Permission(group_id=group.id, module_id=new_module.id,
                                              read=True, create=True, update=True, delete=True))

    db.session.add_all(the_permissions)
    db.session.commit()


def downgrade():
    pass
