#!/usr/bin/env python3
import requests  # type: ignore
import sys
import os

sys.path.append(os.path.join(os.path.expanduser("~"), "master", "libs"))
try:
    import secrets_manager
except ImportError:
    print("Error: Could not import secrets_manager.")
    sys.exit(1)

API_KEY = secrets_manager.get_secret("open_router.key")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_LIST_URL = "https://openrouter.ai/api/v1/models"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def fetch_models():
    """Fetch available models from OpenRouter API."""
    try:
        response = requests.get(MODEL_LIST_URL, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
        return response.json()  # Return the parsed JSON data
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError: {type(e).__name__} - {e}")
        return None

def display_models(data):
    """Display available models and return a dictionary of valid model IDs and their details."""
    print("\n\033[92mAvailable Models:\033[0m\n")
    if not data or not isinstance(data.get("data", []), list):
        print("\033[31mNo models available or invalid response format.")
        return {}

    model_dict = {}
    for model in data.get("data", []):
        model_id = model.get("id", "Unknown ID")
        name = model.get("name", "Unknown Model")
        description = model.get("description", "No description provided.")
        context_length = model.get("context_length", "Unknown")
        pricing = model.get("pricing", {})
        prompt_cost = pricing.get("prompt", "Unknown")
        completion_cost = pricing.get("completion", "Unknown")

        # Add the model to the dictionary
        model_dict[model_id] = {
            "name": name,
            "description": description,
            "context_length": context_length,
            "prompt_cost": prompt_cost,
            "completion_cost": completion_cost
        }

        # Print the model details for readability
        print(f"\033[96mID:\033[0m {model_id}")
        print(f"  \033[94mName:\033[0m {name}")
        print(f"  \033[94mDescription:\033[0m {description}")
        print(f"  \033[94mContext Length:\033[0m {context_length}")
        print(f"  \033[94mPricing:\033[0m Prompt cost: {prompt_cost}, Completion cost: {completion_cost}\n")

    return model_dict

def query(payload):
    """Send a query to the selected OpenRouter model."""
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print("\033[0mRaw API Response:\033[92m", response.json())  # Log the raw response for debugging
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError type: {type(e).__name__}")
        print(f"\033[0mError details: \033[31m{e}")
        # Log the response body if it exists
        if response is not None:
            print("\033[0mResponse body:\033[31m", response.text)
        return None
    except ValueError as ve:
        print(f"\033[31mError: Unable to decode JSON. Details: {ve}")
        return None

def main():
    print("\n\nFetching available models from OpenRouter API...")
    models = fetch_models()
    if not models:
        print("\033[31mFailed to fetch models. Exiting program.")
        return

    # Display models and get the dictionary
    model_dict = display_models(models)

    print("\033[92mYou can choose a model ID from the list above.\033[0m")
    llm_name = input("\033[93mEnter the ID of the model you want to use: \033[0m").strip()

    if llm_name not in model_dict:
        print("\033[31mInvalid model ID. Please restart the program and select a valid model.\033[0m")
        return

    print(f"\nUsing model: \033[93m{model_dict[llm_name]['name']} ({llm_name})\033[0m")
    max_token_price = int(input("Enter max tokens for completion (e.g., 50): "))

    print("\n\nOpenRouter API Program")
    while True:
        print(f"\033[0mThis program processes user input through OpenRouter models. Using model: \033[93m{model_dict[llm_name]['name']}\033[0m")
        user_input = input("\033[92mEnter text for the model to process (type 'exit' to quit): \033[0m")
        if user_input.lower() == 'exit':
            print("Exiting program.")
            break
        payload = {
            "messages": [{"role": "user", "content": user_input}],
            "model": llm_name,
            "max_tokens": max_token_price
        }
        output = query(payload)
        if output and "choices" in output:
            choices = output.get("choices")
            if choices and isinstance(choices, list):
                print("\033[0mResponse:\033[96m", choices[0].get("message").get("content"))
            else:
                print("\033[31mUnexpected API response structure.")
        else:
            print("\033[31mFailed to retrieve a valid response from the API.")

if __name__ == "__main__":
    main()