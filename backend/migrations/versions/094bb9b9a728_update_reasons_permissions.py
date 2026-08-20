"""Update reasons permissions

Revision ID: 094bb9b9a728
Revises: 0d9f90ecd5aa
Create Date: 2026-08-14 15:03:23.371805

"""
import sqlalchemy as sa
from core.app import db
from core.models import Permission


# revision identifiers, used by Alembic.
revision = '094bb9b9a728'
down_revision = '0d9f90ecd5aa'
branch_labels = None
depends_on = None


def upgrade():
    '''Update "reasons" permission module '''

    permissions = db.session.query(Permission)\
        .filter(
            sa.and_(
                Permission.group_id != 1,
                Permission.module_id == 15
            )
        )\
        .all()

    for permission in permissions:
        permission.read = False
        permission.create = False
        permission.delete = False
        permission.update = False

    db.session.commit()


def downgrade():
    pass
