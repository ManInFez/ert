"""Initial state

Revision ID: 14eca8adc993
Revises: cfe785323e50
Create Date: 2020-10-23 08:49:42.892144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "14eca8adc993"
down_revision = "cfe785323e50"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attribute_value",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attribute_value")),
    )
    op.create_table(
        "observation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key_indexes_ref", sa.Integer(), nullable=True),
        sa.Column("data_indexes_ref", sa.Integer(), nullable=True),
        sa.Column("values_ref", sa.Integer(), nullable=True),
        sa.Column("stds_ref", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_observation")),
        sa.UniqueConstraint("name", name="uq_observation_name"),
    )
    op.create_table(
        "parameter_prior",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("group", sa.String(), nullable=True),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("function", sa.String(), nullable=True),
        sa.Column("parameter_names", sa.PickleType(), nullable=True),
        sa.Column("parameter_values", sa.PickleType(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parameter_prior")),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project")),
        sa.UniqueConstraint("name", name="uq_project_name"),
    )
    op.create_table(
        "ensemble",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name=op.f("fk_ensemble_project_id_project")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ensemble")),
        sa.UniqueConstraint(
            "name", "time_created", name="uq_ensemble_name_time_created"
        ),
    )
    op.create_table(
        "observation_attribute",
        sa.Column("observation_id", sa.Integer(), nullable=False),
        sa.Column("attribute", sa.String(), nullable=True),
        sa.Column("value_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["observation_id"],
            ["observation.id"],
            name=op.f("fk_observation_attribute_observation_id_observation"),
        ),
        sa.ForeignKeyConstraint(
            ["value_id"],
            ["attribute_value.id"],
            name=op.f("fk_observation_attribute_value_id_attribute_value"),
        ),
        sa.PrimaryKeyConstraint(
            "observation_id", "value_id", name=op.f("pk_observation_attribute")
        ),
    )
    op.create_table(
        "parameter_definition",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("group", sa.String(), nullable=False),
        sa.Column("ensemble_id", sa.Integer(), nullable=False),
        sa.Column("prior_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
            name=op.f("fk_parameter_definition_ensemble_id_ensemble"),
        ),
        sa.ForeignKeyConstraint(
            ["prior_id"],
            ["parameter_prior.id"],
            name=op.f("fk_parameter_definition_prior_id_parameter_prior"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parameter_definition")),
        sa.UniqueConstraint(
            "name",
            "group",
            "ensemble_id",
            name="uq_parameter_definition_name_group_ensemble_id",
        ),
    )
    op.create_table(
        "prior_ensemble_association_table",
        sa.Column("prior_id", sa.String(), nullable=True),
        sa.Column("ensemble_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
            name=op.f("fk_prior_ensemble_association_table_ensemble_id_ensemble"),
        ),
        sa.ForeignKeyConstraint(
            ["prior_id"],
            ["parameter_prior.id"],
            name=op.f("fk_prior_ensemble_association_table_prior_id_parameter_prior"),
        ),
    )
    op.create_table(
        "realization",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("index", sa.Integer(), nullable=False),
        sa.Column("ensemble_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
            name=op.f("fk_realization_ensemble_id_ensemble"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_realization")),
        sa.UniqueConstraint(
            "index", "ensemble_id", name="uq_realization_index_ensemble_id"
        ),
    )
    op.create_table(
        "response_definition",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("indexes_ref", sa.Integer(), nullable=True),
        sa.Column("ensemble_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ensemble_id"],
            ["ensemble.id"],
            name=op.f("fk_response_definition_ensemble_id_ensemble"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_response_definition")),
        sa.UniqueConstraint(
            "name", "ensemble_id", name="uq_response_definiton_name_ensemble_id"
        ),
    )
    op.create_table(
        "update",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("algorithm", sa.String(), nullable=False),
        sa.Column("ensemble_reference_id", sa.Integer(), nullable=False),
        sa.Column("ensemble_result_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ensemble_reference_id"],
            ["ensemble.id"],
            name=op.f("fk_update_ensemble_reference_id_ensemble"),
        ),
        sa.ForeignKeyConstraint(
            ["ensemble_result_id"],
            ["ensemble.id"],
            name=op.f("fk_update_ensemble_result_id_ensemble"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_update")),
        sa.UniqueConstraint("ensemble_result_id", name="uq_update_result_id"),
    )
    op.create_table(
        "observation_response_definition_link",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("response_definition_id", sa.Integer(), nullable=False),
        sa.Column("active_ref", sa.Integer(), nullable=True),
        sa.Column("observation_id", sa.Integer(), nullable=True),
        sa.Column("update_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["observation_id"],
            ["observation.id"],
            name=op.f(
                "fk_observation_response_definition_link_observation_id_observation"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["response_definition_id"],
            ["response_definition.id"],
            name=op.f(
                "fk_observation_response_definition_link_response_definition_id_response_definition"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["update_id"],
            ["update.id"],
            name=op.f("fk_observation_response_definition_link_update_id_update"),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_observation_response_definition_link")
        ),
        sa.UniqueConstraint(
            "response_definition_id",
            "observation_id",
            "update_id",
            name="uq_observation_response_definition_link_response_definition_id_observation_id_update_id",
        ),
    )
    op.create_table(
        "parameter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value_ref", sa.Integer(), nullable=True),
        sa.Column("realization_id", sa.Integer(), nullable=False),
        sa.Column("parameter_definition_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parameter_definition_id"],
            ["parameter_definition.id"],
            name=op.f("fk_parameter_parameter_definition_id_parameter_definition"),
        ),
        sa.ForeignKeyConstraint(
            ["realization_id"],
            ["realization.id"],
            name=op.f("fk_parameter_realization_id_realization"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parameter")),
        sa.UniqueConstraint(
            "realization_id",
            "parameter_definition_id",
            name="uq_parameter_realization_id_parameter_definition_id",
        ),
    )
    op.create_table(
        "response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("values_ref", sa.Integer(), nullable=True),
        sa.Column("realization_id", sa.Integer(), nullable=False),
        sa.Column("response_definition_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["realization_id"],
            ["realization.id"],
            name=op.f("fk_response_realization_id_realization"),
        ),
        sa.ForeignKeyConstraint(
            ["response_definition_id"],
            ["response_definition.id"],
            name=op.f("fk_response_response_definition_id_response_definition"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_response")),
        sa.UniqueConstraint(
            "realization_id",
            "response_definition_id",
            name="uq_response_realization_id_reponse_defition_id",
        ),
    )
    op.create_table(
        "misfit",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column(
            "observation_response_definition_link_id", sa.Integer(), nullable=True
        ),
        sa.Column("value", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["observation_response_definition_link_id"],
            ["observation_response_definition_link.id"],
            name=op.f(
                "fk_misfit_observation_response_definition_link_id_observation_response_definition_link"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["response.id"],
            name=op.f("fk_misfit_response_id_response"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_misfit")),
        sa.UniqueConstraint(
            "response_id",
            "observation_response_definition_link_id",
            name="uq_misfit_response_id_observation_response_definition_link_id",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("misfit")
    op.drop_table("response")
    op.drop_table("parameter")
    op.drop_table("observation_response_definition_link")
    op.drop_table("update")
    op.drop_table("response_definition")
    op.drop_table("realization")
    op.drop_table("prior_ensemble_association_table")
    op.drop_table("parameter_definition")
    op.drop_table("observation_attribute")
    op.drop_table("ensemble")
    op.drop_table("project")
    op.drop_table("parameter_prior")
    op.drop_table("observation")
    op.drop_table("attribute_value")
    # ### end Alembic commands ###