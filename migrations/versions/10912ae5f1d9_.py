"""empty message

Revision ID: 10912ae5f1d9
Revises: 123a676e5207
Create Date: 2026-05-10 15:01:35.521097
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '10912ae5f1d9'
down_revision = '123a676e5207'
branch_labels = None
depends_on = None


duration_unit_enum = postgresql.ENUM(
    'HOURS', 'DAYS', 'WEEKS',
    name='durationunit',
    create_type=True
)

rental_status_enum = postgresql.ENUM(
    'RESERVED', 'ACTIVE', 'RETURNED', 'CANCELLED', 'OVERDUE',
    name='rentalstatus',
    create_type=True
)

return_reason_enum = postgresql.ENUM(
    'COMPLETED', 'EARLY_RETURN', 'BIKE_ISSUE', 'CUSTOMER_REQUEST',
    name='returnreason',
    create_type=True
)

cancellation_reason_enum = postgresql.ENUM(
    'CUSTOMER_CHANGED_MIND', 'BIKE_UNAVAILABLE',
    'PAYMENT_FAILED', 'ADMIN_CANCELLED',
    name='cancellationreason',
    create_type=True
)


def upgrade():
    bind = op.get_bind()

    # ✅ Create enum types first
    rental_status_enum.create(bind, checkfirst=True)
    duration_unit_enum.create(bind, checkfirst=True)
    return_reason_enum.create(bind, checkfirst=True)
    cancellation_reason_enum.create(bind, checkfirst=True)

    # ✅ Normalize existing data
    op.execute("""
        UPDATE rentals
        SET status = 'ACTIVE'
        WHERE status = 'RENTED'
    """)

    # ✅ Schema changes
    with op.batch_alter_table('rentals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reserved_at', sa.DateTime(timezone=True)))
        batch_op.add_column(sa.Column('rental_start_time', sa.DateTime(timezone=True)))
        batch_op.add_column(sa.Column('actual_return_time', sa.DateTime(timezone=True)))
        batch_op.add_column(sa.Column('cancelled_at', sa.DateTime(timezone=True)))
        batch_op.add_column(sa.Column('duration_value', sa.Integer()))
        batch_op.add_column(
            sa.Column('duration_unit', sa.Enum('HOURS', 'DAYS', 'WEEKS', name='durationunit'))
        )
        batch_op.add_column(
            sa.Column(
                'return_reason',
                sa.Enum('COMPLETED', 'EARLY_RETURN', 'BIKE_ISSUE', 'CUSTOMER_REQUEST', name='returnreason')
            )
        )
        batch_op.add_column(
            sa.Column(
                'cancellation_reason',
                sa.Enum(
                    'CUSTOMER_CHANGED_MIND', 'BIKE_UNAVAILABLE',
                    'PAYMENT_FAILED', 'ADMIN_CANCELLED',
                    name='cancellationreason'
                )
            )
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.VARCHAR(length=20),
            type_=sa.Enum(
                'RESERVED', 'ACTIVE', 'RETURNED', 'CANCELLED', 'OVERDUE',
                name='rentalstatus'
            ),
            postgresql_using="status::rentalstatus",
            existing_nullable=False
        )
        batch_op.alter_column(
            'expected_return_at',
            existing_type=postgresql.TIMESTAMP(),
            type_=sa.DateTime(timezone=True),
            existing_nullable=True
        )


def downgrade():
    bind = op.get_bind()

    with op.batch_alter_table('rentals', schema=None) as batch_op:
        batch_op.alter_column(
            'expected_return_at',
            existing_type=sa.DateTime(timezone=True),
            type_=postgresql.TIMESTAMP(),
            existing_nullable=True
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum(
                'RESERVED', 'ACTIVE', 'RETURNED', 'CANCELLED', 'OVERDUE',
                name='rentalstatus'
            ),
            type_=sa.VARCHAR(length=20),
            existing_nullable=False
        )
        batch_op.drop_column('cancellation_reason')
        batch_op.drop_column('return_reason')
        batch_op.drop_column('duration_unit')
        batch_op.drop_column('duration_value')
        batch_op.drop_column('cancelled_at')
        batch_op.drop_column('actual_return_time')
        batch_op.drop_column('rental_start_time')
        batch_op.drop_column('reserved_at')

    cancellation_reason_enum.drop(bind, checkfirst=True)
    return_reason_enum.drop(bind, checkfirst=True)
    duration_unit_enum.drop(bind, checkfirst=True)
    rental_status_enum.drop(bind, checkfirst=True)