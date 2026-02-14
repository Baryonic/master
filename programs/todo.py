import csv
import os

def load_tasks_from_csv(filename):
    """Load tasks and their priorities from a CSV file."""
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [(row[0], int(row[1])) for row in reader]
    return []

def save_tasks_to_csv(filename, tasks):
    """Save tasks and their priorities to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for task, priority in tasks:
            writer.writerow([task, priority])

def main():
    filename = "todo2.csv"
    tasks = load_tasks_from_csv(filename)  # Load tasks from the CSV file

    while True:
        # Display the menu
        print("\n\033[94m------TASK PLANNER-------- \033[0m keyday_electronics\n")
        print("\033[95m1. Print To-Do Tasks")
        print("\033[96m2. Add a New Task")
        print("\033[95m3. Print Tasks by Priority")
        print("\033[92m4. Complete a Task")
        print("\033[31m5. Exit \033[0m")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            # Print all tasks
            if not tasks:
                print("\nNo tasks in your to-do list.")
            else:
                print("\nTo-Do Tasks:")
                for index, (task, priority) in enumerate(tasks, start=1):
                    priority_text = {1: "High Priority", 2: "Normal", 3: "Chill"}.get(priority, "Unknown")
                    print(f"{index}. {task} ({priority_text})")
        elif choice == '2':
            # Add a new task
            new_task = input("\nEnter the new task: ")
            while True:
                try:
                    priority = int(input("Enter the priority (1 = High, 2 = Normal, 3 = Chill): "))
                    if priority in [1, 2, 3]:
                        break
                    else:
                        print("Invalid priority. Please choose 1, 2, or 3.")
                except ValueError:
                    print("Please enter a valid number.")
            tasks.append((new_task, priority))
            save_tasks_to_csv(filename, tasks)  # Save tasks to the CSV file
            print(f"Task '{new_task}' added with priority {priority}.")
        elif choice == '3':
            # Print tasks by priority
            try:
                priority = int(input("\nEnter the priority to filter by (1 = High, 2 = Normal, 3 = Chill): "))
                if priority in [1, 2, 3]:
                    filtered_tasks = [(task, p) for task, p in tasks if p == priority]
                    if not filtered_tasks:
                        print("\nNo tasks found for the selected priority.")
                    else:
                        print("\nFiltered Tasks:")
                        for index, (task, _) in enumerate(filtered_tasks, start=1):
                            print(f"{index}. {task}")
                else:
                    print("Invalid priority. Please choose 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            # Complete a task
            if not tasks:
                print("\nNo tasks to complete.")
            else:
                print("\nTo-Do Tasks:")
                for index, (task, priority) in enumerate(tasks, start=1):
                    priority_text = {1: "High Priority", 2: "Normal", 3: "Chill"}.get(priority, "Unknown")
                    print(f"{index}. {task} ({priority_text})")
                try:
                    task_number = int(input("Enter the number of the task to complete: "))
                    if 1 <= task_number <= len(tasks):
                        completed_task, _ = tasks.pop(task_number - 1)
                        save_tasks_to_csv(filename, tasks)  # Save tasks to the CSV file
                        print(f"Task '{completed_task}' completed and removed from the list.")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == '5':
            # Exit the program
            print("Exiting the task planner. Have a productive day!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
