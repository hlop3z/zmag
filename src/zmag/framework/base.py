from spoc import Framework, Schema, Hook
from config import settings

from ..builder.models import build_models

# Define the application schema
schema = Schema(
    # Modules to load from each app
    modules=["models", "api", "tools", "commands"]
)

# Create the framework instance
framework = Framework(
    base_dir=settings.BASE_DIR,
    schema=schema,
    echo=False,  # Set to True for debug output
    mode="loose",  # "strict" enforces all modules exist, "loose" allows missing
)


# Access registered components
build_models(framework.components.models.items())
