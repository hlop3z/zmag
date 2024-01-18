from typing import Callable
import logging
import json
import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_data = {
            "timestamp": timestamp,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


def setup_json_logging(logger_name, log_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Remove existing handlers (if any)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Create a console handler and set the formatter to JSON
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)
    return logger


# Usage:
logger = setup_json_logging("DatabaseAPI")


class DatabaseManager:
    def __init__(self, table):
        self.table = table

    def query(self, items: list = None):
        try:
            if not items:
                return None
            return self.table.query_list(items)
        except:  # noqa: E722
            return None

    def queryset_bind(self, current, next):
        if type(current).__name__ != "NoneType" and type(next).__name__ != "NoneType":
            current &= next
        elif type(current).__name__ != "NoneType":
            return current
        return next

    async def compare_and_filter_objects(self, new: dict, old: dict) -> dict:
        common_keys = set(new.keys()).intersection(old.keys())
        filtered_object = {key: new[key] for key in common_keys}
        return filtered_object

    async def get_objects_by_ids(
        self, list_of_ids: list, check_object: Callable = None
    ):
        selected_ids = [self.table.id_decode(x) for x in list_of_ids]
        rows_query = self.table.query_list([["_id", "in", selected_ids]])
        rows = await self.table.find_all(rows_query, sort_by="-id")

        if check_object:
            if rows.data:
                return [
                    x
                    for x in [await check_object(item) for item in rows.data]
                    if x is not None
                ]
            else:
                return []
        else:
            return rows.data

    async def update(
        self,
        list_of_ids: list,
        form: dict,
        object_perms_method: Callable = None,
        is_many: bool = False,
    ):
        if not isinstance(list_of_ids, list):
            list_of_ids = [list_of_ids]

        rows = await self.get_objects_by_ids(list_of_ids, object_perms_method)

        updated_ids = []
        object_list = []

        for row in rows:
            row_dict = {**row.__dict__}
            updates_dict = await self.compare_and_filter_objects(form, row_dict)
            row_dict.update(updates_dict)
            updated_ids.append(row_dict.get("id"))
            object_list.append(row_dict)

        results = await self.table.update(updated_ids, form, ignore_return=True)
        if results.error:
            logger.error(results.error_message)

        if is_many:
            return object_list
        else:
            if len(object_list) == 1:
                return object_list[0]
            else:
                return None

    async def create(self, form: dict | list):
        results = await self.table.create(form)
        if results.error:
            logger.error(results.error_message)
        if isinstance(form, list):
            if results.data:
                return [x.__dict__ for x in results.data]
            return []
        else:
            if results.data:
                return results.data.__dict__
            return results.data

    async def detail(self, item_detail_id: str, object_perms_method: Callable = None):
        results = await self.table.detail(item_detail_id)
        row = {}
        if results:
            if object_perms_method:
                is_allowed = await object_perms_method(results)
                if is_allowed:
                    row = results.__dict__
            else:
                row = results.__dict__
        return row

    async def delete(
        self,
        list_of_ids: list | str,
        object_perms_method: Callable = None,
    ):
        if not isinstance(list_of_ids, list):
            list_of_ids = [list_of_ids]

        if object_perms_method:
            rows = await self.get_objects_by_ids(list_of_ids, object_perms_method)
            deleted_ids = [row.id for row in rows]
            results = await self.table.delete(deleted_ids)
            if results.error:
                logger.error(results.error_message)
            return deleted_ids
        else:
            results = await self.table.delete(list_of_ids)
            if results.error:
                logger.error(results.error_message)

            return list_of_ids

    async def find(
        self,
        client_query: object = None,
        perms_query: object = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "-id",
        get_all: bool = False,
    ):
        query = self.queryset_bind(client_query, perms_query)

        if type(self.table).__name__ == "Mongo" and not query:
            query = {}

        if get_all:
            results = await self.table.find_all(
                query,
                sort_by=sort_by,
            )
        else:
            results = await self.table.find(
                query,
                page=page,
                limit=limit,
                sort_by=sort_by,
            )
        return results

    async def filter(
        self,
        client_queryset: list = None,
        perms_queryset: Callable = None,
        object_perms_method: Callable = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "-id",
        get_all: bool = False,
    ):
        client_query = None
        perms_query = None
        if client_queryset:
            client_query = self.query(client_queryset)
        if perms_queryset:
            perms_query = await perms_queryset(self)
        results = await self.find(
            client_query,
            perms_query,
            page=page,
            limit=limit,
            sort_by=sort_by,
            get_all=get_all,
        )

        if object_perms_method:
            if results.data:
                rows = [
                    x
                    for x in [await object_perms_method(item) for item in results.data]
                    if x is not None
                ]
                results.data = rows
        if results.data:
            results.data = [x.__dict__ for x in results.data]
        return results
