#!/usr/bin/env python3
import requests #type:ignore 
import sys
import os

sys.path.append(os.path.join(os.path.expanduser("~"), "master", "libs"))
try:
    import secrets_manager
except ImportError:
    print("Error: Could not import secrets_manager.")
    sys.exit(1)

API_KEY = secrets_manager.get_secret("hugging_face.key")

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError type: {type(e).__name__}")
        print(f"\033[0mError details: \033[31m{e}")
        if response is not None and response.text:
            print("\033[0mResponse body:\033[31m", response.text)
        return None

def main():
    print("\n \n Free Api Key by Hugging Face ")
    while True:
        print("\033[0mthis program runs slowly while the LLM is processing the answer")
        user_input = input("\033[92mEnter text for the model to process (type 'exit' to quit): \033[0m")
        if user_input.lower() == 'exit':
            print("Exiting program.")
            break
        output = query({"inputs": user_input})
        if output:
            print("Response:\033[91m", output)
        else:
            print("\033[31mFailed to retrieve a response.")


if __name__ == "__main__":
    main()
