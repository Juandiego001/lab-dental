"""Update users photo path

Revision ID: 8114f453f7a3
Revises: 41ec0f6cead3
Create Date: 2026-09-25 12:43:46.070593

"""
from alembic import op
import sqlalchemy as sa
from core.app import db
from core.models import User


# revision identifiers, used by Alembic.
revision = '8114f453f7a3'
down_revision = '41ec0f6cead3'
branch_labels = None
depends_on = None


def upgrade():
    users = db.session.query(User).filter(User.photo != None).all()
    for user in users:
        user.photo = user.photo.replace('./users_files/', '')
        db.session.add(user)

    db.session.commit()


def downgrade():
    pass
