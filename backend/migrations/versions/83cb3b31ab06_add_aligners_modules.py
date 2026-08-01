"""Add Aligners modules

Revision ID: 83cb3b31ab06
Revises: d65c528f1e43
Create Date: 2026-07-31 12:44:10.495370

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import Module, Permission


# revision identifiers, used by Alembic.
revision = '83cb3b31ab06'
down_revision = 'd65c528f1e43'
branch_labels = None
depends_on = None


def upgrade():
    '''Add aligners modules'''

    module = Module(name='aligners')
    db.session.add(module)
    db.session.flush()

    permission = Permission(
        group_id=1,
        module_id=module.id,
        read=True,
        create=True,
        update=True,
        delete=True)
    db.session.add(permission)
    db.session.commit()


def downgrade():
    pass
