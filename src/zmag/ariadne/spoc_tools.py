try:
    import spoc
except ImportError:
    spoc = None


from .resource_api import ResourcesAPI


# Model
def type(name):
    """
    Model Definition:

    This function defines a model with the specified `kebab-case-name`.

    Example:
    ```
    >>> Author = model("book-author")
    ```

    Usage Examples:

    - Define a field for the model:

    ```
    @Author.field("full_name")
    async def resolve_full_name(obj, info):
        return obj.get("first_name", "") + " " + obj.get("last_name", "")
    ```

    - Specify permissions for the model ('update', 'delete', 'detail', 'filter'):

    ```
    @Author.perms("update")
    async def check_object_perms(obj, info):
        user_id = info.context.get("user_id")
        if obj.user_id != user_id:
            return None
        return obj
    ```

    - Define actions to be performed after operations ('create', 'update', 'delete', 'detail', 'filter'):

    ```
    @Author.after("filter")
    async def after_method(response, info):
        print("After everything is ready and done")
    ```

    - Specify filter options for the model ('computed', 'query'):

    ```
    @Author.filter("computed")
    async def dataset_computed_value(response, info):
        return {"computed_value": len(response.data)}

    @Author.filter("query")
    async def preset_query(lookup, context=None):
        perms_query = lookup.query([
            ["last_name", "contains", "doe"],
            "or",
            ["last_name", "contains", "crichton"],
        ])
        perms_query &= lookup.query([["_id", "eq", 1])
        return perms_query
    ```

    - Define forms ('create', 'update'):

    ```
    @Author.form("update")
    class Update:
        first_name = zmag.value(
            str,
            default=None,
            required=False,
            # rules=[(lambda v: v.lower().startswith("j") or "invalid input")],
            filters=zmag.filters(
                rules=[(lambda v: v.lower())],
            ),
        )
        last_name = zmag.value(
            str,
            required=True,
            filters=zmag.filters(
                rules=[(lambda v: v.lower())],
            ),
        )
    ```


    Args:
    - `name` (str): The name of the model.

    Returns:
    - ResourcesAPI: An instance of the ResourcesAPI class with the specified core utilities and name.
    """
    core_utils = ["field", "perms", "filter", "after", "form"]

    cls = ResourcesAPI(*core_utils, name=name)
    if spoc:
        spoc.component(cls, config={}, metadata={"type": "model_resource"})
    return cls
