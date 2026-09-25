"""subject deep lessons

Revision ID: 38a101bfa821
Revises: 25033ff1da00
Create Date: 2026-09-25 16:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '38a101bfa821'
down_revision: Union[str, None] = '25033ff1da00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = Inspector.from_engine(bind)
    tables = insp.get_table_names()

    # Drop temporary alembic table if left over
    if '_alembic_tmp_subjects' in tables:
        op.execute(sa.text("DROP TABLE IF EXISTS _alembic_tmp_subjects"))

    # 1. Update subjects
    subject_cols = [c['name'] for c in insp.get_columns('subjects')]
    with op.batch_alter_table('subjects', schema=None) as batch_op:
        if 'category' not in subject_cols:
            batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=True, server_default='COMPUTER_SCIENCE'))
        if 'difficulty_level' not in subject_cols:
            batch_op.add_column(sa.Column('difficulty_level', sa.String(length=20), nullable=True, server_default='BEGINNER'))
        if 'thumbnail_url' not in subject_cols:
            batch_op.add_column(sa.Column('thumbnail_url', sa.String(length=255), nullable=True))
        if 'display_order' not in subject_cols:
            batch_op.add_column(sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
        if 'is_active' not in subject_cols:
            batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))
        if 'created_at' not in subject_cols:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
        if 'updated_at' not in subject_cols:
            batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # 2. Update lessons
    lesson_cols = [c['name'] for c in insp.get_columns('lessons')]
    with op.batch_alter_table('lessons', schema=None) as batch_op:
        if 'short_description' not in lesson_cols:
            batch_op.add_column(sa.Column('short_description', sa.String(length=255), nullable=True))
        if 'detailed_description' not in lesson_cols:
            batch_op.add_column(sa.Column('detailed_description', sa.Text(), nullable=True))
        if 'difficulty_level' not in lesson_cols:
            batch_op.add_column(sa.Column('difficulty_level', sa.String(length=20), nullable=True, server_default='MEDIUM'))
        if 'estimated_duration' not in lesson_cols:
            batch_op.add_column(sa.Column('estimated_duration', sa.Integer(), nullable=True, server_default='15'))
        if 'lesson_order' not in lesson_cols:
            batch_op.add_column(sa.Column('lesson_order', sa.Integer(), nullable=False, server_default='0'))
        if 'display_order' not in lesson_cols:
            batch_op.add_column(sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
        if 'is_active' not in lesson_cols:
            batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))
        if 'created_at' not in lesson_cols:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
        if 'updated_at' not in lesson_cols:
            batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # 3. Update topics
    topic_cols = [c['name'] for c in insp.get_columns('topics')]
    with op.batch_alter_table('topics', schema=None) as batch_op:
        if 'lesson_id' not in topic_cols:
            batch_op.add_column(sa.Column('lesson_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key('fk_topics_lesson_id', 'lessons', ['lesson_id'], ['id'], ondelete='SET NULL')
            batch_op.create_index('ix_topics_lesson_id', ['lesson_id'])
        if 'display_order' not in topic_cols:
            batch_op.add_column(sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
        if 'is_active' not in topic_cols:
            batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))
        if 'created_at' not in topic_cols:
            batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
        if 'updated_at' not in topic_cols:
            batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # 4. Create study_resources if not exists
    if 'study_resources' not in tables:
        op.create_table(
            'study_resources',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('lesson_id', sa.Integer(), nullable=False),
            sa.Column('topic_id', sa.Integer(), nullable=True),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('url', sa.String(length=500), nullable=False),
            sa.Column('resource_type', sa.String(length=50), nullable=False, server_default='DOCUMENTATION'),
            sa.Column('provider', sa.String(length=100), nullable=False, server_default='EXTERNAL'),
            sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='SET NULL'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_study_resources_id'), 'study_resources', ['id'], unique=False)
        op.create_index(op.f('ix_study_resources_lesson_id'), 'study_resources', ['lesson_id'], unique=False)
        op.create_index(op.f('ix_study_resources_topic_id'), 'study_resources', ['topic_id'], unique=False)
        op.create_index(op.f('ix_study_resources_title'), 'study_resources', ['title'], unique=False)


def downgrade() -> None:
    pass
