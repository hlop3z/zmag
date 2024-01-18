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


def get_filter_page(response):
    return response.data.get("filter", {}).get("page", {})


def test_filter():
    request = {
        "page": 1,
        "sort": "-id",
        "all": True,
    }
    response = client.filter(MODEL_NAME, context=CONTEXT, **request)
    print(response.data)


def test_next():
    request = {
        "page": 1,
        "limit": 1,
        "sort": "-id",
    }
    response = client.filter(MODEL_NAME, context=CONTEXT, **request)
    print(get_filter_page(response))


def test_prev():
    request = {
        "page": 2,
        "limit": 1,
        "sort": "-id",
    }
    response = client.filter(MODEL_NAME, context=CONTEXT, **request)
    print(get_filter_page(response))


def test_all():
    test_filter()
    test_next()
    test_prev()


if __name__ == "__main__":
    # test_all()
    print(
        {
            "page": None,
            "limit": None,
            "sort": None,
            "all": None,
        }
    )
