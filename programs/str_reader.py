import pyttsx3 # type: ignore

def speak_text(text):
    try:
        engine = pyttsx3.init()  # Initialize the TTS engine
        engine.say(text)  # Queue the text to be spoken
        engine.runAndWait()  # Process the queue and speak the text
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    try:
        user_input = input("Enter a string to be read aloud: ")
        if not user_input.strip():  # Check if input is empty or whitespace
            raise ValueError("Input cannot be empty. Please provide valid text.")
        speak_text(user_input)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
