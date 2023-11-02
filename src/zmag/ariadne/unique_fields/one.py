from types import SimpleNamespace
from ..jsql import Util


############################################
# Unique (One)
############################################
def unique_query_list_or(table, client_form):
    unique_keys = table.config.get("unique", [])
    unique_query_list = []
    unique_form = {}

    for index, key in enumerate(unique_keys):
        value = client_form.get(key)
        unique_form[key] = value
        unique_query_list.append([key, "eq", value])
        if index < len(unique_keys) - 1:
            unique_query_list.append("or")

    return SimpleNamespace(
        query=table.database.objects.query_list(unique_query_list),
        form=unique_form,
    )


async def check_object_is_unique(table, client_form):
    unique_admin = unique_query_list_or(table, client_form)
    unique_results = await table.database.objects.find_one(unique_admin.query)
    unique_errors = []
    if unique_results:
        unique_results_dict = unique_results.__dict__
        for key, val in unique_admin.form.items():
            other_val = unique_results_dict.get(key)
            if other_val == val:
                unique_errors.append(
                    {
                        "field": Util.snake_to_camel(key),
                        "type": "unique",
                        "text": "value error",
                    }
                )
    return unique_errors


############################################
# Unique-Together (One)
############################################0
def build_query_for_unique_together(key_pair, client_form):
    query_list = []
    for index, key in enumerate(key_pair):
        value = client_form.get(key)
        query_list.append([key, "eq", value])
        if index < len(key_pair) - 1:
            query_list.append("and")
    return query_list


def unique_query_list_and(table, client_form):
    unique_keys = table.config.get("unique_together", [])
    unique_query_list = []

    for index, key_pair in enumerate(unique_keys):
        query_list = build_query_for_unique_together(key_pair, client_form)
        unique_query_list.extend(query_list)

        if index < len(unique_keys) - 1:
            unique_query_list.append("or")

    return table.database.objects.query_list(unique_query_list)


async def check_object_is_unique_together(table, client_form):
    unique_query = unique_query_list_and(table, client_form)
    unique_results = await table.database.objects.find_one(unique_query)

    if unique_results:
        unique_keys = table.config.get("unique_together", [])
        unique_keys_flat_set = set(item for sublist in unique_keys for item in sublist)
        unique_results_dict = unique_results.__dict__
        unique_together_errors = []

        for key in unique_keys_flat_set:
            current = unique_results_dict.get(key)
            if current == client_form.get(key):
                unique_together_errors.append(
                    {
                        "field": Util.snake_to_camel(key),
                        "type": "unique_together",
                        "text": "value error",
                    }
                )

        return unique_together_errors
