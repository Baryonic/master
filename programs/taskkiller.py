import psutil
import curses
import time

# Number of programs to display
NUM_PROGRAMS = 39  # Display 39 programs

# Dictionary to map two-digit Task IDs to PIDs
id_to_pid_map = {}
pid_to_id_map = {}  # Reverse map for tracking if a PID already has an assigned ID

# List of protected program names
protected_programs = ["explorer.exe", "Unknown"]

# List of programs safe to kill
safe_to_kill_programs = ["Copilot.exe", "Taskmgr.exe", "ProtonVPNService.exe", "Discord.exe", "Telegram.exe"]

def display_task_manager(screen):
    """
    Dynamically displays the top processes consuming the most RAM and allows the user to terminate tasks.
    Updates every 0.2 seconds, and ensures Task IDs remain consistent even if the process order changes.
    Protected and safe-to-kill programs are explicitly marked in the table.
    """
    curses.curs_set(0)  # Hide the cursor
    screen.nodelay(False)  # Wait for user input when necessary
    screen.timeout(-1)  # Wait indefinitely for input when in prompt mode

    while True:
        # Clear the screen
        screen.clear()

        # Get all processes and sort by memory usage
        processes = sorted(psutil.process_iter(['pid', 'name', 'memory_info']),
                           key=lambda p: p.info['memory_info'].rss if p.info['memory_info'] else 0,
                           reverse=True)[:NUM_PROGRAMS]

        # Display headers
        screen.addstr(0, 0, f"{'Task ID':<10}{'Program Name':<30}{'RAM Used (MB)':<15}{'Protected':<10}{'Safe to Kill':<15}")
        screen.addstr(1, 0, "-" * 85)

        # Display the top processes and ensure consistent Task ID mapping
        for i, process in enumerate(processes):
            try:
                pid = process.info['pid']
                name = process.info['name'] if process.info['name'] else "Unknown"
                ram_used = process.info['memory_info'].rss / (1024 ** 2)  # Convert bytes to MB
                is_protected = "Yes" if name in protected_programs else ""
                is_safe_to_kill = "Yes" if name in safe_to_kill_programs else ""

                # Assign a consistent two-digit Task ID if not already assigned
                if pid not in pid_to_id_map:
                    task_id = f"{len(id_to_pid_map) + 1:02}"  # Generate next two-digit ID
                    id_to_pid_map[task_id] = pid
                    pid_to_id_map[pid] = task_id
                else:
                    task_id = pid_to_id_map[pid]

                # Display process information
                screen.addstr(i + 2, 0, f"{task_id:<10}{name:<30}{ram_used:<15.2f}{is_protected:<10}{is_safe_to_kill:<15}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Instructions for quitting or killing tasks
        screen.addstr(NUM_PROGRAMS + 2, 0, "(Press 'q' to quit, 'k' to kill a task)")

        # Refresh the screen
        screen.refresh()

        # Get user input
        key = screen.getch()

        # Quit on 'q'
        if key == ord('q'):
            break

        # Kill a task on 'k'
        if key == ord('k'):
            screen.addstr(NUM_PROGRAMS + 3, 0, "Enter Task ID to terminate: ")
            curses.echo()  # Enable user input display
            task_id = screen.getstr(NUM_PROGRAMS + 3, 26).decode("utf-8").strip()  # Read and decode input
            curses.noecho()  # Disable user input display after reading

            # Attempt to terminate the process 
            try:
                if task_id in id_to_pid_map:
                    pid = id_to_pid_map[task_id]
                    process = psutil.Process(pid)
                    name = process.name()
                    if name in protected_programs:
                        screen.addstr(NUM_PROGRAMS + 4, 0, f"Task {task_id} ({name}) is protected and cannot be terminated!")
                    elif name in safe_to_kill_programs:
                        process.terminate()  # Terminate the process
                        del id_to_pid_map[task_id]
                        del pid_to_id_map[pid]  # Remove mappings
                        screen.addstr(NUM_PROGRAMS + 4, 0, f"Task {task_id} (PID {pid}, {name})\033[92m terminated successfully!\033[0m")
                    else:
                        screen.addstr(NUM_PROGRAMS + 4, 0, f"Task {task_id} ({name})\033[31m cannot be terminated unless marked safe.\033[0m")
                else:
                    screen.addstr(NUM_PROGRAMS + 4, 0, f"\033[31mFailed to find Task ID {task_id}.\033[0m")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                screen.addstr(NUM_PROGRAMS + 4, 0, f"\033[31mFailed to terminate Task ID {task_id}:\033[0m {e}")

            screen.refresh()
            time.sleep(1)  # Pause briefly to display the result

if __name__ == "__main__":
    print("Starting Task Manager... (Press 'q' to quit, 'k' to kill a task)")
    try:
        curses.wrapper(display_task_manager)
    except KeyboardInterrupt:
        print("\n\033[31mTask Manager stopped. Goodbye!")        