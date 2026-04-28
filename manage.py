from zmag.framework import framework


def main():
    """Run the application."""
    print("\n=== SPOC Application Started ===\n")

    # Access installed apps
    print(f"Installed apps: {framework.installed_apps}")

    # Get all models
    print("\n--- Registered Models ---")
    if hasattr(framework.components, "models"):
        for name, model in framework.components.models.items():
            print(f"  • {name}: {model}")

    # Get all views
    print("\n--- Registered Views ---")
    if hasattr(framework.components, "views"):
        for name, view in framework.components.views.items():
            print(f"  • {name}: {view}")

    # Get a specific component
    print("\n--- Using Components ---")
    list_posts = framework.get_component("views", "blog.list_posts")
    if list_posts:
        result = list_posts()
        print(f"list_posts() returned: {result}")

    print("\n=== Application Running ===\n")

    # When done, shutdown gracefully
    framework.shutdown()
    print("\n=== Application Stopped ===\n")


if __name__ == "__main__":
    main()
