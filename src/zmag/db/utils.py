from sqlalchemy import asc, desc


def apply_sort(model, query, sort_fields, allowed_fields):
    order_clauses = []

    for field in sort_fields:
        desc_order = field.startswith("-")
        col_name = field[1:] if desc_order else field

        if col_name not in allowed_fields:
            continue  # or raise error

        column = getattr(model, col_name)
        order_clauses.append(desc(column) if desc_order else asc(column))

    return query.order_by(*order_clauses)
