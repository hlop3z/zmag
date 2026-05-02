from types import SimpleNamespace
from typing import Any
from dataclasses import dataclass
from sqlalchemy import (
    DateTime,
    Index,
    UniqueConstraint,
    Column,
    ForeignKey,
    Table,
    func,
)
from spoc import get_info


from ..core.decorators.models import SQLMeta
from ..db.metadata import METADATA
from ..db.tables import ORM, M2MORM


@dataclass
class SQL:
    columns: list[Any]
    uniques: list[Any]
    indexes: list[Any]
    m2m: dict[str, Link]


@dataclass
class Link:
    name: str
    field_name: str
    left_col: str
    right_col: str
    left: Any
    right: Any


@dataclass
class Form:
    create: list[str]
    update: list[str]
    required: list[str]
    nullable: list[str]


def create_index(app_label, fields: tuple[str, ...]):
    return Index(f"ix_{app_label}_{'_'.join(fields)}", *fields)


def create_unique(fields: tuple[str, ...]):
    return UniqueConstraint(*fields, name=f"uq_{'_'.join(fields)}")


def process_fields(app_label, table_name, meta) -> SQL:
    raw_columns = []  # (sort_order, column)
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
        if m2m and sql_ref and ref_model:
            own_ref = f"{table_name}.id"
            own_col_name = f"{table_name[len(app_label)+1:]}_id"
            ref_col_name = f"{ref_model.lower()}_id"
            left, right = sorted([sql_ref, own_ref])
            link_name = f"m2m_{left.split('.')[0]}_{right.split('.')[0]}"
            left_col = own_col_name if left == own_ref else ref_col_name
            right_col = ref_col_name if left == own_ref else own_col_name
            relationships[link_name] = Link(
                name=link_name,
                field_name=field.name,
                left_col=left_col,
                right_col=right_col,
                left=Column(left_col, ForeignKey(left), primary_key=True),
                right=Column(right_col, ForeignKey(right), primary_key=True),
            )
        elif sql_col is not None:
            order = field.metadata.get("order", 0)
            raw_columns.append((order, sql_col(field.name, sql_ref)))

    columns = [col for _, col in sorted(raw_columns, key=lambda x: x[0])]

    # Meta
    for args in meta.index:
        columns_index.append(create_index(app_label, args))
    for args in meta.unique:
        columns_unique.append(create_unique(args))

    return SQL(
        columns=columns,
        uniques=columns_unique,
        indexes=columns_index,
        m2m=relationships,
    )


def build_models(models_list):
    relationship = {}
    model_m2m_refs = {}  # link_name -> [(model, field_name), ...]
    for name, model in models_list:
        # Give each model its own orm class and m2m namespace (not shared via inheritance)
        model.orm: ORM = type("orm", (ORM,), {})
        model.m2m: M2MORM = type("m2m", (M2MORM,), {})

        info = get_info(model)

        meta: SQLMeta = info.config.get("sql")  # type: ignore
        table_name = name.lower().replace(".", "_")
        apps_label = name.split(".")[0].lower()
        table_info = process_fields(apps_label, table_name, meta)

        for link_name, link in table_info.m2m.items():
            if link_name not in relationship:
                relationship[link_name] = link
            model_m2m_refs.setdefault(link_name, []).append((model, link.field_name))

        # ORM Attach
        model.orm.sortable = meta.sortable or []
        model.orm.table = Table(
            table_name,
            METADATA,
            *table_info.columns,
            *table_info.indexes,
            *table_info.uniques,
        )

    # Create each junction table once, then attach a per-perspective subclass to each model
    for link_name, link in relationship.items():
        m2m_table = Table(
            link_name,
            METADATA,
            link.left,
            link.right,
            Column("created_at", DateTime, server_default=func.now(), nullable=False),
        )

        for owner_model, field_name in model_m2m_refs.get(link_name, []):
            own_table_name = owner_model.orm.table.name
            own_col: str | None = None
            related_col: str | None = None
            related_table_name: str = ""

            for col in m2m_table.columns:
                if not col.foreign_keys:
                    continue
                fk_target = next(iter(col.foreign_keys)).target_fullname.split(".")[0]
                if fk_target == own_table_name:
                    own_col = col.name
                else:
                    related_col = col.name
                    related_table_name = fk_target

            m2m_orm = type(
                "m2m",
                (M2MORM,),
                {
                    "table": m2m_table,
                    "related_table": METADATA.tables[related_table_name],
                    "own_col": own_col,
                    "related_col": related_col,
                },
            )
            setattr(owner_model.m2m, field_name, m2m_orm)

    return relationship
