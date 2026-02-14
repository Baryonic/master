#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# --- Configuration ---
MASTER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(MASTER_DIR, "programs")
SECRETS_DIR = os.path.join(MASTER_DIR, "secrets")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(script_name):
    """Runs a python script located in the programs directory."""
    script_path = os.path.join(BASE, script_name)
    
    if not os.path.exists(script_path):
        print(f"\033[31mError: Script not found: {script_path}\033[0m")
        time.sleep(2)
        return

    try:
        # Save current directory
        original_cwd = os.getcwd()
        
        # Change to script directory so it can find its local assets/modules if any
        os.chdir(BASE)
        
        print(f"\033[36mRunning: {script_name}...\033[0m")
        time.sleep(0.5)
        
        # Determine python command
        python_cmd = "python" if os.name == 'nt' else "python3"
        
        # Run using python command
        subprocess.run([python_cmd, script_path], check=False)
        
        # Restore directory
        os.chdir(original_cwd)
        
    except KeyboardInterrupt:
        print("\n\033[33mScript interrupted by user.\033[0m")
    except Exception as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")
    
    input("\nPress Enter to return to menu...")

def display_menu():
    clear_screen()
    print("\n\033[34m=== \033[94mMaster Pro\033[36mgram Menu \033[35m=== \033[96mLinux Edition \033[37m")
    print("\033[38;2;255;180;100m 1: Run Learning Tracker (learningtracker.py)")
    print("\033[93m 2: Run Task Planner (todo.py)")
    print("\033[36m 3: Print useful Commands (commands.py)")
    print("\033[92m 4: PCstats (stats.py)")
    print("\033[95m 5: SGX Auto (sgx_auto_01.py)")
    print("\033[33m 6: STR reader (str_reader.py)")
    print("\033[33m 7: Hangman (hangman.py)")
    print("\033[36m 8: Timer (timer.py)")
    print("\033[95m 9: Alpaca Trading BTC (trademenu.py) \033[31mNOT FREE")
    print("\033[91m10: PROGRAMS (programs.py)")
    print("\033[92m11: Task Killer (taskkiller.py)")
    print("\033[38;2;25;255;120m12: Keydate (keydate.py)")
    print("\033[91m13: Hugging Face 1.0 (hugging_face_gpt.py)\033[92m free")
    print("\033[91m14: Wifi Networks (wifi_networks.py)")
    print("\033[91m15: Wifi 2 (wifi2.py)")
    print("\033[96m16: Gemini Short Answer (or1.py) \033[92m free")
    print("\033[96m17: Gemini 2.5 (or4.py)\033[92m free" )
    print("\033[95m18: OpenRouter Model Explorer (or3.py) \033[31mNOT FREE")
    print("\033[96m19: OpenRouter Comparator (or5.py) \033[92mFREE")
    print("\033[96m20: OpenRouter Logic/Tester (freemodeltester.py)")
    print("\033[91m21: OpenRouter Image Model Tester (llm_imgs1.py) \033[92mfree")
    print("\033[96m22: Auto LLM Tester (free_auto_llm_tester.py) \033[92mfree")
    print("\033[38;2;255;150;230m77: Run master.py as subprocess")
    print("\033[38;2;255;200;189m78: Add New Program (npf.py)")
    print("\033[38;2;200;100;100m79: Program Editor (program_editor.py)")
    print("\033[31m89: SHUTDOWN PC (shutdown.py)")
    print("99: Exit")
    print("\033[0m===========================\n")

def main():
    while True:
        display_menu()
        
        try:
            choice_input = input("Enter option: ").strip()
            if not choice_input:
                continue
            choice = int(choice_input)
            
            if choice == 1:
                run_script("learningtracker.py")
            elif choice == 2:
                run_script("todo.py")
            elif choice == 3:
                run_script("commands.py")
            elif choice == 4:
                run_script("stats.py")
            elif choice == 5:
                run_script("sgx_auto_01.py")
            elif choice == 6:
                run_script("str_reader.py")
            elif choice == 7:
                run_script("hangman.py")
            elif choice == 8:
                run_script("timer.py")
            elif choice == 9:
                run_script("trademenu.py")
            elif choice == 10:
                run_script("programs.py")
            elif choice == 11:
                run_script("taskkiller.py")
            elif choice == 12:
                run_script("keydate.py")
            elif choice == 13:
                run_script("hugging_face_gpt.py")
            elif choice == 14:
                run_script("wifi_networks.py")
            elif choice == 15:
                run_script("wifi2.py")
            elif choice == 16:
                run_script("or1.py")
            elif choice == 17:
                run_script("or4.py")
            elif choice == 18:
                run_script("or3.py")
            elif choice == 19:
                run_script("or5.py")
            elif choice == 20:
                run_script("freemodeltester.py")
            elif choice == 21:
                run_script("llm_imgs1.py")
            elif choice == 22:
                run_script("free_auto_llm_tester.py")
            elif choice == 77:
                print("Spawning subprocess...")
                python_cmd = "python" if os.name == 'nt' else "python3"
                subprocess.run([python_cmd, os.path.join(MASTER_DIR, "master.py")])
            elif choice == 78:
                run_script("npf.py")
            elif choice == 79:
                if os.path.exists(os.path.join(BASE, "program_editor.py")):
                    run_script("program_editor.py")
                else:
                    print(f"program_editor.py not found in {BASE}")
                    time.sleep(2)
            elif choice == 89:
                run_script("shutdown.py")
            elif choice == 99:
                print("\033[31mExiting Master Program. Goodbye!\033[0m")
                sys.exit(0)
            else:
                print("Invalid choice.")
                time.sleep(1)
        except ValueError:
            print("Invalid input. Please enter a number.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
