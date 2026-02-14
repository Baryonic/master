from datetime import datetime

def calavera_art():
    # Get the current time
    current_time = datetime.now()

    # Extract hours and minutes
    hours = current_time.hour
    minutes = current_time.minute
    day=current_time.day
    month=current_time.month
    year=current_time.year
    if day<10:
        day=(f"0{day}")
    if month<10:
        month=(f"0{month}")
    print(f"\033[31mkeydate   ⣀⣀⣠⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⢠⣦⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⢸⣿⣿⣿⣦⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣦⣈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⢸⣿⣿⣿⡿⠋⠻⣿⣿⣷⣦⣤⣉⠉⠛⠛⠛⠛⠋⠁⢰⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⢸⣿⣿⣿⣇\033[94m{hours}\033[31m ⠈⠉⣹⣿⣿⡆⠀\033[94m{minutes}\033[31m  ⠀⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠙⠻⣿⣿⣷⣦⣤⣤⣾⣿⡿⠹⣷⡀⠀⠀⠀⢀⣼⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⠃⠀⢻⣿⣷⣶⣾⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣇⣀⣈⣿⣿⣿⣿⠃⠀⠀____⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡉⠛⠻⠿⠿⠿⠟⠛⢉⡁⠀⠀|\033[94m{day}\033[31m|___⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿{year}⢰⣶⣶⠀⣿⣧⠀⠀⠀ |\033[94m{month}\033[31m|⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⡉⠀⠈⠛⠀⠸⠿⠋⠀⢉⣠⣄⠀⠀⠀|?⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣿⣿⣷⣶⣶⣤⣤⣤⣤⣶⠟⠃⠀⠀⠀:|:⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print(f"⠀⠀⠀⠀      ⠀⠈⠉⠉⠛⠛⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀|uwu⠀⠀⠀⠀⠀⠀⠀⠀")


def main():
    calavera_art()
    waiter=input(f"\033[0mpress \033[92menter\033[0m to continue")



if __name__=="__main__":
    main()