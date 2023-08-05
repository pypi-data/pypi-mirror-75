"""Add indices

Revision ID: 9010a64e5a2d
Revises: 306266361f4f
Create Date: 2019-11-27 21:31:33.868141

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '9010a64e5a2d'
down_revision = '306266361f4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_playlist_episode_id'), 'playlist', ['episode_id'], unique=False)
    op.create_index(op.f('ix_playlist_for_client'), 'playlist', ['for_client'], unique=False)
    op.create_index(op.f('ix_playlist_project_id'), 'playlist', ['project_id'], unique=False)
    op.create_index(op.f('ix_task_assigner_id'), 'task', ['assigner_id'], unique=False)
    op.create_index(op.f('ix_task_task_status_id'), 'task', ['task_status_id'], unique=False)
    op.create_index(op.f('ix_task_task_type_id'), 'task', ['task_type_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_type_id'), table_name='task')
    op.drop_index(op.f('ix_task_task_status_id'), table_name='task')
    op.drop_index(op.f('ix_task_assigner_id'), table_name='task')
    op.drop_index(op.f('ix_playlist_project_id'), table_name='playlist')
    op.drop_index(op.f('ix_playlist_for_client'), table_name='playlist')
    op.drop_index(op.f('ix_playlist_episode_id'), table_name='playlist')
    # ### end Alembic commands ###
