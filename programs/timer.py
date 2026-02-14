import time
import threading
import datetime
import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def play_alarm(frequency, sample_rate=44100):
    duration = 1  # Short bursts of 1 second
    while True:
        sine_wave = generate_sine_wave(frequency, duration)
        sd.play(sine_wave, samplerate=sample_rate)
        sd.wait()  # Wait until the sound is finished
        if stop_alarm.is_set():
            break

def timer_countdown(seconds):
    total_time = seconds
    while seconds > 0:
        progress = int(((total_time - seconds) / total_time) * 30)  # Progress bar size = 30
        loading_bar = "[" + "#" * progress + "-" * (30 - progress-1) + "]"
        time_left = round(seconds, 1)  # Display seconds with 1 decimal precision
        print(f"\r{loading_bar} {time_left} seconds({round((time_left/60), 2)}minutes)", end="")
        time.sleep(0.1)  # Update the loading bar every 0.1 seconds
        seconds -= 0.1
    print("\n\033[31mTime's up!")

def main():
    global stop_alarm
    stop_alarm = threading.Event()

    try:
        # Input time in minutes (fractional values allowed)
        minutes = float(input("Enter the number of minutes for the timer: "))
        seconds = minutes * 60

        # Calculate and display the end time
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(seconds=seconds)
        print(f"Timer set for {minutes:.2f} minute(s). The alarm will sound at {end_time.strftime('%H:%M:%S')}.")

        # Start the countdown in a separate thread
        countdown_thread = threading.Thread(target=timer_countdown, args=(seconds,))
        countdown_thread.start()

        # Wait for the timer to complete
        countdown_thread.join()
        
        print("Time's up! Alarm is playing...")

        # Start the alarm in a separate thread
        frequency = 440  # Frequency in Hz (A4 note)
        alarm_thread = threading.Thread(target=play_alarm, args=(frequency,))
        alarm_thread.start()

        # Wait for user input to stop the alarm
        input("Press \033[92mEnter\033[31m to stop the alarm.")
        stop_alarm.set()  # Signal the alarm thread to stop
        alarm_thread.join()  # Wait for the alarm thread to finish

        print("\033[0mAlarm stopped.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
