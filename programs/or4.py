#!/usr/bin/env python3
import requests  # type: ignore
import os
import sys

sys.path.append(os.path.join(os.path.expanduser("~"), "master", "libs"))
try:
    import secrets_manager
except ImportError:
    print("Error: Could not import secrets_manager.")
    sys.exit(1)

API_KEY = secrets_manager.get_secret("open_router.key")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
model_id = "google/gemini-2.5-pro-exp-03-25"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError type: {type(e).__name__}")
        print(f"\033[0mError details: \033[31m{e}")
        if 'response' in locals():  # Ensure response exists before accessing its properties
            print("\033[0mResponse body:\033[31m", response.text)
        return {"choices": [{"message": {"content": "Error: API request failed."}}]}  # Avoid NoneType errors

def main():
    print(f"\n\n \033[95mOpenRouter API Program, using \033[0m{model_id}")
    while True:
        print("\033[0mAsk an efficient question\033[31m Doesn't remember past responses!\033[93mno format")
        user_input = input("\033[92mEnter text for the model to process (type 'exit' to exit): \033[0m")
        if user_input.lower() == 'exit' or user_input.lower()=="quit":
            print("Exiting program.")
            break
        
        payload = {
            "messages": [{"role": "user", "content": f"{user_input}"}],
            "model": model_id,  # Specify the model to use
            "max_tokens": 5000  # Limit response length
        }
        
        output = query(payload)
        
        # Ensure output has expected data structure before accessing keys
        if output and "choices" in output and output["choices"]:
            print("Response:\033[94m", output["choices"][0]["message"]["content"])
        else:
            print("\033[31mFailed to retrieve a valid response.")

if __name__ == "__main__":
    main()