from zmag.framework.base import framework

from apps.sample_app.models import Blog, User

# Access registered components
print(framework.components.models.get("sample.Blog"))

# Blog
b_data = Blog(name="my-blog")
print(b_data.id)

# Blog
u_data = User(first_name="john")
print(u_data.id)
