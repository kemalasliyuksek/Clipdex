from clipdex_core.listener import ClipdexListener

def main():
    """
    Main entry point of the application.
    For now, it only starts the keyboard listener engine.
    """
    try:
        clipdex_engine = ClipdexListener()
        clipdex_engine.start()
        clipdex_engine.join()  # Prevents the main thread from exiting
    except KeyboardInterrupt:
        print("\nShutting down Clipdex.")
    except Exception as e:
        # Especially on macOS, this error can occur if permissions are missing
        print(f"Failed to start the application. Error: {e}")
        print("If you are using macOS, ensure that the application has 'Accessibility' and 'Input Monitoring' permissions.")


if __name__ == "__main__":
    main()