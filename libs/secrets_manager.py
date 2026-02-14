import os

# Get the directory where this script (secrets_manager.py) is located: .../master/libs
LIBS_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to .../master, then into 'secrets'
SECRETS_DIR = os.path.join(os.path.dirname(LIBS_DIR), "secrets")

def get_secret(key_name):
    """
    Retrieves a secret from the secrets directory.
    key_name: The name of the file containing the secret (e.g., 'alpaca.key').
    """
    path = os.path.join(SECRETS_DIR, key_name)
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return f.read().strip()
        except IOError as e:
            print(f"Error reading secret {key_name}: {e}")
            return None
    else:
        print(f"Secret file not found: {path}")
        return None
