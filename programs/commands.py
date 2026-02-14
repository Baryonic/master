import csv
import os

def load_commands_from_csv(filename):
    """Load commands from a CSV file."""
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    return []

def save_commands_to_csv(filename, commands):
    """Save commands to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for command in commands:
            writer.writerow([command])

def main():
    filename = "commands.csv"
    commands = load_commands_from_csv(filename)  # Load commands from the CSV file

    while True:
        print("\n=== Command List ===")
        
        # Display all commands
        if not commands:
            print("No commands found.")
        else:
            print("Commands:")
            for index, command in enumerate(commands, start=1):
                print(f"{index}. {command}")
        
        print("\nOptions:")
        print("1: Add a New Command")
        print("2: Exit")

        choice = input("Choose an option (1-2): ").strip()

        if choice == '1':
            new_command = input("Enter the new command: ").strip()
            commands.append(new_command)
            save_commands_to_csv(filename, commands)  # Save the updated commands to the CSV file
            print(f"Command '{new_command}' added.")
        elif choice == '2':
            print("Exiting the program. Have a great day!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
