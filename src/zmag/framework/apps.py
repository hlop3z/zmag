"""Main application entry point."""

from config import settings
from spoc import Framework, Hook, Schema

from .builders.models import build_models

# Define the application schema
schema = Schema(
    # Modules to load from each app
    modules=["models", "api"],
    # Module dependencies (views depend on models)
    dependencies={
        "api": ["models"],
    },
    # Lifecycle hooks
    hooks={
        "models": Hook(
            startup=lambda m: print(f"✓ Loaded models: {m}"),
            shutdown=lambda m: print(f"✗ Unloading models: {m}"),
        ),
        "api": Hook(
            startup=lambda m: print(f"✓ Loaded views: {m}"),
            shutdown=lambda m: print(f"✗ Unloading views: {m}"),
        ),
    },
)

# Create the framework instance
framework = Framework(
    base_dir=settings.BASE_DIR,
    schema=schema,
    echo=False,  # Set to True for debug output
    mode="loose",  # "strict" enforces all modules exist, "loose" allows missing
)


build_models(framework.components.models.items())
