# ZMAG **Requests**

This example demonstrates how to make GraphQL requests using ZMAG’s `Frontend` class.

```python
from zmag import Frontend

client = Frontend(
    host="tcp://127.0.0.1:5555",  
    mode="queue",  
    is_sync=False,  
)
```

---

## **GraphQL Request**

ZMAG allows you to send GraphQL queries or mutations to a remote service. Below is an example of how to perform a GraphQL query using the `request` method.

```python
GQL_QUERY = """
query MyQuery($title: String) {
  bookDetail(title: $title) {
    id
    title
  }
}
"""

response = await client.request(
    query=GQL_QUERY,  # The GraphQL query to be executed
    variables={
        "title": "Jurassic Park",  # Pass any required query variables
    },
    operation="MyQuery",  # Name of the GraphQL operation
    context={
        "user": {  # Provide additional context, such as user data
            "id": 1,
            "username": "admin",
            "is_staff": True,
            "is_active": True,
            "is_superuser": True,
            "is_authenticated": True,
        }
    },
)

# Output the result of the GraphQL request
print(response.body["data"])
```

---

### **Explanation**

- **GQL_QUERY**: The GraphQL query is defined as a string, and it includes a parameter `$title` to query for a book by title.
- **`variables`**: The variables required by the query are passed as a dictionary, in this case, the title `"Jurassic Park"`.
- **`operation`**: Specifies the name of the GraphQL operation (`"MyQuery"`).
- **`context`**: Allows you to send additional data, such as user information, with the request.
- **`response.body["data"]`**: This is where you access the returned data from the GraphQL server.

This example provides a flexible way to integrate GraphQL queries within a ZMAG environment.
