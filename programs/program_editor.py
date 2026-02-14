# New Python file+
import os

# Define the folder path
folder_path = "python/master programs"

# Get a list of Python files in the folder
python_files = [f for f in os.listdir(folder_path) if f.endswith(".py")]

# Display the list of Python files
if not python_files:
    print("No Python files found in the folder.")
else:
    print("Available Python programs:")
    for i, file in enumerate(python_files, start=1):
        print(f"{i}. {file}")

    # Prompt the user for a selection
    while True:
        try:
            choice = int(input("\nEnter the number corresponding to the program (or 99 to cancel): "))
            if choice == 99:
                print("Operation cancelled.")
                break
            elif 1 <= choice <= len(python_files):
                selected_file = python_files[choice - 1]
                os.system(f'code "{folder_path}/{selected_file}"')  # Open in VS Code
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")