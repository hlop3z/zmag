from types import SimpleNamespace
from ..jsql import Util


# Unique (Many)
def unique_query_list_or(table, client_forms):
    unique_keys = table.config.get("unique", [])
    unique_query_list = []
    unique_forms = []

    form_grouped = {}
    for client_form in client_forms:
        form = {}
        for key in unique_keys:
            value = client_form.get(key)
            if key not in form_grouped:
                form_grouped[key] = []
            form_grouped[key].append(value)
            form[key] = value
        unique_forms.append(form)

    for index, key in enumerate(unique_keys):
        unique_query_list.append([key, "in", form_grouped[key]])
        if index < len(unique_keys) - 1:
            unique_query_list.append("or")

    return SimpleNamespace(
        query=table.database.objects.query_list(unique_query_list),
        forms=unique_forms,
    )


async def check_object_is_unique_many(table, client_forms):
    unique_admin = unique_query_list_or(table, client_forms)
    unique_errors = []
    unique_results = await table.database.objects.find_one(unique_admin.query)
    matching_key = None

    if unique_results:
        dict_one = unique_results.__dict__
        for key, value in dict_one.items():
            for dict_two in unique_admin.forms:
                if key in dict_two and dict_two[key] == value:
                    matching_key = key
                    break
            if matching_key:
                break

    if matching_key:
        unique_errors.append(
            {
                "field": Util.snake_to_camel(matching_key),
                "type": "unique",
                "text": "value error",
            }
        )

    return unique_errors


# Unique-Together (Many)
def build_query_for_unique_together(table, client_forms):
    unique_keys = table.config.get("unique_together", [])
    unique_query_list = []
    unique_forms = []
    unique_keys_flat_set = set(item for sublist in unique_keys for item in sublist)

    form_grouped = {}
    for client_form in client_forms:
        for group_name in unique_keys_flat_set:
            value = client_form.get(group_name)
            if not form_grouped.get(group_name):
                form_grouped[group_name] = []
            form_grouped[group_name].append(value)

    for index, key in enumerate(unique_keys_flat_set):
        unique_query_list.append([key, "in", form_grouped[key]])
        if index < len(unique_keys_flat_set) - 1:
            unique_query_list.append("and")

    return SimpleNamespace(
        query=table.database.objects.query_list(unique_query_list),
        forms=unique_forms,
        keys=unique_keys_flat_set,
    )


async def check_object_is_unique_together_many(table, client_forms):
    unique_query = build_query_for_unique_together(table, client_forms)
    unique_results = await table.database.objects.find_one(unique_query.query)

    unique_together_errors = []
    if unique_results:
        unique_results_dict = unique_results.__dict__
        for client_form in client_forms:
            for key in unique_query.keys:
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
