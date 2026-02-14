#THIS PROGRAM SHOULD BE STORED IN THE PARENT DIRECTORY OF /"master programs"

import os
import subprocess

def main():
    try:
        # Prompt the user for the file name
        file_name = input("Enter the name of the new Python file: ").strip()
        if not file_name:
            raise ValueError("No file name provided. Please enter a valid file name.")
        
        # Append the .py extension if it's not provided
        if not file_name.lower().endswith('.py'):
            file_name += '.py'
        
        # Define the directory (assumed to already exist)
        directory = "master programs"
        
        # Verify that the directory exists.
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")
        
        # Construct the full path for the new file
        file_path = os.path.join(directory, file_name)
        
        # Check if a file with the same name already exists
        if os.path.exists(file_path):
            raise FileExistsError(f"A file named '{file_name}' already exists in '{directory}'.")
        
        # Create the new file with a basic header
        with open(file_path, 'w') as f:
            f.write("# New Python file\n\n")
        
        # Enclose the file path in quotes to handle spaces in directory names properly.
        command = f'code "{file_path}"'
        subprocess.run(command, shell=True, check=True)
        
        print(f"File '{file_name}' has been created and opened in Visual Studio Code successfully.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()