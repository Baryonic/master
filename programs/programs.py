import subprocess

def launch_program(program_path):
    """
    Launches a Windows program given its path.

    Parameters:
        program_path (str): The full path to the program executable.

    Returns:
        None
    """
    try:
        subprocess.Popen(program_path)
        print(f"Program at '{program_path}' launched successfully!")
    except FileNotFoundError:
        print(f"Program not found: {program_path}")
    except Exception as e:
        print(f"Error occurred: {e}")

def display_menu():
    """
    Displays a menu to select and launch a program.
    """
    print("Choose a program to open:")
    print("1. Telegram")
    print("2. VPN")
    print("3. COPILOT")
    print("4. Program4")
    print("5. Program5")
    print("99. Exit")

def main():
    # Paths to the programs
    programs = {
        1: r"C:\Users\cex\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Telegram Desktop\Telegram",
        2: r"C:\Program Files\Proton\VPN\ProtonVPN.Launcher.exe",
        3: r"C:\Program Files\WindowsApps\Microsoft.Copilot_1.25032.167.0_x64__8wekyb3d8bbwe\Copilot.exe",
        4: r"C:\Path\To\Program4.exe",
        5: r"C:\Path\To\Program5.exe"
    }

    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice (1-6): "))
            if choice == 99:
                print("Exiting the program. Goodbye!")
                break
            elif choice in programs:
                launch_program(programs[choice])
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()