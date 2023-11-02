from .one import check_object_is_unique, check_object_is_unique_together
from .many import (
    check_object_is_unique_many,
    check_object_is_unique_together_many,
)


async def unique_object(table, client_form):
    # Check Unique
    unique_errors = await check_object_is_unique(table, client_form)
    if not isinstance(unique_errors, list):
        unique_errors = unique_errors or []
    if len(unique_errors) > 0:
        return {"error": {"messages": unique_errors}}
    # Check (Unique Together)
    unique_together_errors = await check_object_is_unique_together(table, client_form)
    unique_together_errors = unique_together_errors or []
    if len(unique_together_errors) > 0:
        return {"error": {"messages": unique_together_errors}}
    return None


async def unique_object_many(table, clean_forms):
    # Check Unique
    unique_errors = await check_object_is_unique_many(table, clean_forms)
    if not isinstance(unique_errors, list):
        unique_errors = unique_errors or []
    if len(unique_errors) > 0:
        return {"error": {"messages": unique_errors}}

    # Check (Unique Together)
    unique_together_errors = await check_object_is_unique_together_many(
        table, clean_forms
    )
    unique_together_errors = unique_together_errors or []
    if len(unique_together_errors) > 0:
        return {"error": {"messages": unique_together_errors}}
    return None
