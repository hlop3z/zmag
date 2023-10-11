class BaseManager:
    """Reusable Database Manager"""

    @classmethod
    async def reset_table(cls):
        return await cls.objects.delete(None, all=True)

    @classmethod
    def filter_query_by_user_id(cls, active_query, user_id):
        table = cls.objects
        if type(active_query).__name__ != "NoneType":
            return (active_query) & table.where("user_id", "eq", user_id)
        else:
            return table.where("user_id", "eq", user_id)

    @classmethod
    async def get_ids_by_user_id(cls, selected, user_id):
        table = cls.objects
        if not isinstance(selected, list):
            selected = [selected]
        selected = {table.id_decode(x): x for x in selected}
        active_query = table.Q.where("_id", "in", list(selected.keys()))
        active_query = cls.filter_query_by_user_id(active_query, user_id)
        results = await table.database.fetch_all(table.Q.select(active_query))
        return [selected[item._id] for item in results]

    @classmethod
    async def search(
        cls,
        context,
        pagination=None,
        query=None,
    ):
        return await cls.objects.find(
            query,
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 10),
            sort_by=pagination.get("sort_by", "-id"),
        )

    @classmethod
    async def detail(cls, context, id=None, query=None):
        return await cls.objects.find_one(query)

    @classmethod
    async def create(cls, context, form=None):
        return await cls.objects.create(form)

    @classmethod
    async def update(cls, context, selected=None, form=None):
        return await cls.objects.update(selected, form)

    @classmethod
    async def delete(cls, context, selected=None):
        return await cls.objects.delete(selected)
