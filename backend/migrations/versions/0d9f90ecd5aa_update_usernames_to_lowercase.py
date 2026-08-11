"""Update usernames to lowercase

Revision ID: 0d9f90ecd5aa
Revises: 83cb3b31ab06
Create Date: 2026-08-11 09:34:46.419930

"""
from core.app import db
from alembic import op
import sqlalchemy as sa

from core.models import User


# revision identifiers, used by Alembic.
revision = '0d9f90ecd5aa'
down_revision = '83cb3b31ab06'
branch_labels = None
depends_on = None


def upgrade():
    pass

    users = db.session.query(User).filter(User.status == 'ACTIVE')
    for user in users:
        user.username = user.username.lower()
        user.email = user.email.lower()

    db.session.commit()


def downgrade():
    pass
