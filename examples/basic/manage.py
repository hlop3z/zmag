from typing import Any
from dataclasses import dataclass

from zmag import framework
from zmag.framework.sql_model import SQLMeta
from spoc import get_info

from sqlalchemy import Index, UniqueConstraint, Column, ForeignKey


"""
association_table = Table(
    "association",
    metadata,
    Column("left_id", ForeignKey("left.id"), primary_key=True),
    Column("right_id", ForeignKey("right.id"), primary_key=True),
)
"""


@dataclass
class SQL:
    columns: list[Any] | None = None
    uniques: list[str] | None = None
    indexes: list[str] | None = None
    m2m: list[str] | None = None


@dataclass
class Link:
    name: str
    left: Any
    right: Any


@dataclass
class Form:
    create: list[str]
    update: list[str]
    required: list[str]
    nullable: list[str]


def create_index(app_label, fields: tuple[str, ...]):
    return Index(f"ix_{app_label}_{''.join(fields)}", *fields)


def create_unique(app_label, fields: tuple[str, ...]):
    return UniqueConstraint(*fields, name=f"uq_{app_label}_{''.join(fields)}")


def process_fields(app_label, table_name, meta) -> SQL:
    columns = []
    relationships = []
    columns_index = []
    columns_unique = []
    for field in meta.fields:
        sql_col = field.metadata.get("sql")
        _ref = field.metadata.get("refs")
        m2m = field.metadata.get("many_to_many")
        sql_ref = None
        ref_model = None
        if _ref:
            ref_label, ref_model, col_ref = _ref.split(".")
            sql_ref = f"{ref_label}_{ref_model}.{col_ref}".lower()
        if m2m and sql_ref:
            left, right = sorted([sql_ref, f"{table_name}.id"])
            link_name = f"m2m_{left.split('.')[0]}_{right.split('.')[0]}"
            relationships.append(
                Link(
                    name=link_name,
                    left=Column("left_id", ForeignKey(left), primary_key=True),
                    right=Column("right_id", ForeignKey(right), primary_key=True),
                )
            )
        else:
            columns.append(sql_col(field.name, sql_ref))

    # Meta
    for args in meta.index:
        columns_index.append(create_index(app_label, args))
    for args in meta.unique:
        columns_unique.append(create_unique(app_label, args))

    return SQL(
        columns=columns,
        uniques=columns_unique,
        indexes=columns_index,
        m2m=relationships,
    )

    # SQL(m2m=sql_ref)


def main():
    """Run the application."""
    print("\n=== SPOC Application Started ===\n")

    # Access installed apps
    print(f"Installed apps: {framework.installed_apps}")

    # Get all models
    print("\n--- Registered Models ---")
    relationship = []
    for name, model in framework.components.models.items():
        print(f"  • {name}: {model}")
        info = get_info(model)
        meta: SQLMeta = info.config.get("sql")  # type: ignore
        table_name = name.lower().replace(".", "_")
        apps_label = name.split(".")[0].lower()
        table_info = process_fields(apps_label, table_name, meta)
        relationship.append(table_info.m2m)
        print(table_info.columns)
        print(table_info.indexes)
        print(table_info.uniques)

    # Get a specific component
    print("\n--- Using Components ---")
    found_model = framework.get_component("models", "sample.User")
    if found_model:
        print(f"Model: {found_model}")

    print("\n=== Application Running ===\n")
    # When done, shutdown gracefully
    # framework.shutdown()


if __name__ == "__main__":
    main()
