from typing import Any
from dataclasses import dataclass
from sqlalchemy import Index, UniqueConstraint, Column, ForeignKey, MetaData, Table
from spoc import get_info


from ...framework.sql_model import SQLMeta

METADATA = MetaData()


@dataclass
class SQL:
    columns: list[Any]
    uniques: list[Any]
    indexes: list[Any]
    m2m: dict[str, Link]


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
    relationships = {}
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
            print(field)
            relationships[link_name] = Link(
                name=link_name,
                left=Column("left_id", ForeignKey(left), primary_key=True),
                right=Column("right_id", ForeignKey(right), primary_key=True),
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


def build_models(models_list):
    relationship = {}
    for name, model in models_list:
        info = get_info(model)

        meta: SQLMeta = info.config.get("sql")
        table_name = name.lower().replace(".", "_")
        apps_label = name.split(".")[0].lower()
        table_info = process_fields(apps_label, table_name, meta)
        relationship.update(table_info.m2m)

        # ORM Attach
        model.orm.table = Table(
            table_name,
            METADATA,
            *table_info.columns,
            *table_info.indexes,
            *table_info.uniques,
        )

    return relationship
