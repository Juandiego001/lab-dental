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
    conn = op.get_bind()
    query = sa.text(
        "SELECT id, photo FROM users WHERE photo IS NOT NULL")
    results = conn.execute(query).fetchall()

    update_data = []
    for row in results:
        user_id = row[0]
        user_photo = row[1].replace('./users_files/', '')
        update_data.append({
            "id": user_id,
            "photo": user_photo,
        })

    query = sa.text("UPDATE users SET photo = :photo WHERE id = :id")
    conn.execute(query, update_data)


def downgrade():
    pass
