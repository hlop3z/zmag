from .base import framework


def get_model(app_label: str, model_name: str):
    return framework.get_component("models", f"{app_label}.{model_name}")


def get_models():
    return framework.components.models.items()
