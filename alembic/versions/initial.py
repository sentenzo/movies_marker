"""initial

Revision ID: 1f03e274ae9a
Revises: 180bbf4fd65e
Create Date: 2022-09-17 18:27:14.378211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1f03e274ae9a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.execute("""DROP TYPE markschema CASCADE""")

    op.create_table(
        "movie",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__movie")),
    )
    op.create_unique_constraint(op.f("uq__movie__title"), "movie", ["title"])

    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
    )
    op.create_table(
        "marks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("movie", sa.Integer(), nullable=False),
        sa.Column(
            "mark",
            sa.Enum("AWESOME", "GREAT", "GOOD", "NOT_BAD", "BAD", name="markschema"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["movie"],
            ["movie.id"],
            name=op.f("fk__marks__movie__movie"),
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["user.id"],
            name=op.f("fk__marks__user__user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__marks")),
    )


def downgrade() -> None:

    op.drop_constraint(op.f("uq__movie__title"), "movie", type_="unique")
    op.execute("""DROP TYPE markschema CASCADE""")

    op.drop_table("marks")
    op.drop_table("user")
    op.drop_table("movie")
    ...
