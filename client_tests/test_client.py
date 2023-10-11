import asyncio

from zmg_client import ZMQ

query = """
fragment ModelFields on Book {
  id
  author
  title
  books
}

fragment PageFields on PageInfo {
  extra
  length
  pages
}

fragment ErrorFields on Error {
  error
  meta
  messages {
    field
    text
    type
  }
}

query Detail($id: ID!) {
  BookDetail(id: $id) {
    ...ModelFields
  }
}

query Search($pagination: Pagination!) {
  BookSearch(pagination: $pagination) {
    pageInfo {
      ...PageFields
    }
    edges {
      node {
        ...ModelFields
      }
    }
  }
}

mutation Create($form: FormBookCreate!) {
  BookCreate(form: $form, forms: null) {
    item {
      ...ModelFields
    }
    error {
      ...ErrorFields
    }
  }
}

mutation CreateMany($forms: [FormBookCreate!]) {
  BookCreate(form: null, forms: $forms) {
    items {
      ...ModelFields
    }
    error {
      ...ErrorFields
    }
  }
}

mutation Update($id: ID, $form: FormBookUpdate!) {
  BookUpdate(item: {id: $id}, form: $form) {
    item {
      ...ModelFields
    }
    error {
      ...ErrorFields
    }
  }
}

mutation UpdateMany($ids: [ID!], $form: FormBookUpdate!) {
  BookUpdate(item: {ids: $ids}, form: $form) {
    updated
    error {
      ...ErrorFields
    }
  }
}

mutation Delete($ids: [ID!]) {
  BookDelete(item: {ids: $ids}) {
    deleted
  }
}
"""


async def test_client():
    proxy = ZMQ()
    # Client
    proxy.client()

    for i in range(1):
        # Request
        request = {
            "query": query,
            "operation": "Search",
            "variables": {
                "id": "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
                "form": {"author": "F. Scott Fitzgerald", "title": "The Great Gatsby"},
                "pagination": {"page": 1, "limit": 100, "sortBy": "-id", "all": False},
                "query": {
                    "name": "helloworld",
                    "amount": "10.1",
                    "count": 10,
                    "cash": 1.5,
                    "endDatetime": "2022-11-10T16:35:56.216344",
                    "startDate": "2022-11-10",
                    "timestamp": "16:35:04.872130",
                },
            },
        }

        # Response
        response = await proxy.request({"token": "someTokenForUser"}, **request)
        print(response)


async def main():
    await asyncio.gather(test_client())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
