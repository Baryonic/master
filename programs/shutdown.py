import os

def shutdown_computer():
    """Immediately shuts down the computer."""
    os.system("shutdown /s /t 0")

if __name__ == "__main__":
    print("Shutting down the computer...")
    shutdown_computer()
