from zmag import framework


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

    # Get a specific component
    print("\n--- Using Components ---")
    found_model = framework.get_component("models", "sample.User")
    if found_model:
        print(f"Model: {found_model}")

    print("\n=== Application Running ===\n")
    # When done, shutdown gracefully
    # framework.shutdown()


if __name__ == "__main__":
    main()
