from zmag.client import Client
from pathlib import Path

CURRENT_PATH = Path(__file__).parent


"""
type Query {
  info: ServerInfo
  detail(model: String!, id: ID): DetailResponse
  filter(...args): FilterResponse
}

type Mutation {
  create(model: String!, form: Form!): EditorResponse
  update(model: String!, form: Form!): EditorResponse
  createMany(model: String!, forms: [Form!]): EditManyResponse
  updateMany(model: String!, ids: [ID!], form: Form!): EditManyResponse
  delete(model: String!, ids: [ID!]): DeleteResponse
}
"""


client = Client(
    # host="tcp://127.0.0.1:5555",
    base_dir=CURRENT_PATH,
    fragments={"Author": "fragments/author.graphql"},
)

MODEL_NAME = "Author"
CONTEXT = {
    "user_id": 123,
}


def test_info():
    response = client.info(context=CONTEXT)
    print(response)


def test_create():
    form_create = {
        "firstName": "John",  # John Michael Jane
        "lastName": "Doe",  # Doe Crichton Lopez
    }
    response = client.create(MODEL_NAME, form=form_create, context=CONTEXT)
    print(response)


def test_update():
    form_update = {
        "id": "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
        # "firstName": "Jane",
        "lastName": "Crichton",
    }
    response = client.update(MODEL_NAME, form=form_update, context=CONTEXT)
    print(response)


def test_delete():
    item_ids = [
        "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
        "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
        "Mzo6NGQ0MDk4MzIxNjU0YTQ1Nw==",
    ]
    response = client.delete(MODEL_NAME, ids=item_ids, context=CONTEXT)
    print(response)


def test_detail():
    item_id = "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ=="
    response = client.detail(MODEL_NAME, id=item_id, context=CONTEXT)
    print(response)


def test_filter():
    response = client.filter(MODEL_NAME, context=CONTEXT)
    print(response)


def test_create_many():
    form_create_many = [
        {
            "firstName": "Michael",
            "lastName": "Crichton",
        },
        {
            "firstName": "Jane",  # Michael Jane
            "lastName": "Lopez",  # Crichton Lopez
        },
    ]
    response = client.create_many(MODEL_NAME, forms=form_create_many, context=CONTEXT)
    print(response)


def test_update_many():
    item_ids = [
        "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
        "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
    ]
    form_update_many = {
        # "firstName": "Jane",
        "lastName": "Doe",
    }
    response = client.update_many(
        MODEL_NAME, ids=item_ids, form=form_update_many, context=CONTEXT
    )
    print(response)


def test_all():
    # CU One
    test_create()
    test_update()
    # CU Many
    test_create_many()
    test_update_many()
    # Read
    test_detail()
    test_filter()
    # Delete One or Many
    test_delete()
    # Info
    test_info()


if __name__ == "__main__":
    test_all()
