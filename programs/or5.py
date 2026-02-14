#!/usr/bin/env python3
import csv
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
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_models_from_csv(file_path):
    """
    Load models from a CSV file and assign them numeric IDs, properly extracting
    the model ID, description, and parameters.

    The CSV file is expected to have rows with:
      - Column 0: model_id (always present)
      - Column 1: description (optional)
      - Column 2: parameters (optional)

    For example:
      meta-llama/llama-3.1-405b:free
      mistralai/mistral-nemo:free, "multilingual"
      microsoft/phi-4-reasoning:free, "logic and maths", "14B"
    """
    models = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader, start=1):
                if not row or not row[0].strip():
                    continue  # Skip empty lines
                
                # Use the CSV reader's columns directly.
                model_id = row[0].strip()
                description = row[1].strip() if len(row) > 1 and row[1].strip() else "No description"
                parameters = row[2].strip() if len(row) > 2 and row[2].strip() else "Unknown"
                
                models[idx] = {
                    "model_id": model_id,
                    "description": description,
                    "parameters": parameters
                }
        return models
    except FileNotFoundError:
        print("\033[31mError: CSV file not found. Ensure `llm_ids.csv` exists in the current directory.\033[0m")
        return {}

def display_models(models):
    """Display models in a formatted table."""
    print("\n\033[92mAvailable Models:\033[0m\n")
    if not models:
        print("\033[31mNo models found.\033[0m")
        return

    print(f"{'ID':<5} {'Model ID':<50} {'Description':<30} {'Parameters':<10}")
    print("-" * 100)
    for num, details in models.items():
        print(f"{num:<5} {details['model_id']:<50} {details['description']:<30} {details['parameters']:<10}")

def query_model(model_id, user_input, max_tokens):
    """Send user query to OpenRouter API and return both processed and raw response."""
    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": model_id,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        raw_data = response.json()
        
        if raw_data and "choices" in raw_data:
            choices = raw_data.get("choices", [])
            if choices and isinstance(choices, list):
                processed_response = choices[0].get("message", {}).get("content", "No response.")
            else:
                processed_response = "\033[31mError: Invalid API structure.\033[0m"
        else:
            processed_response = "\033[31mError: No valid response received.\033[0m"

        return processed_response, raw_data
    except requests.exceptions.RequestException as e:
        return f"\033[31mAPI Request Error: {e}\033[0m", {}

def main():
    models = load_models_from_csv("llm_ids.csv")
    if not models:
        print("\033[31mNo models loaded. Exiting.\033[0m")
        return

    # Initially display the available models
    display_models(models)

    while True:
        choice = input("\033[93mSelect a model ID (or 'exit' to quit): \033[0m").strip()
        if choice.lower() in ["exit", "quit"]:
            print("\033[31mExiting program.\033[0m")
            break
        if not choice.isdigit() or int(choice) not in models:
            print("\033[31mInvalid choice. Please enter a valid numeric model ID.\033[0m")
            continue

        selected_model = models[int(choice)]
        print(f"\nUsing model: \033[93m{selected_model['model_id']}\033[0m - {selected_model['description']} ({selected_model['parameters']})\n")
        
        try:
            max_tokens = int(input("Enter max tokens for completion (e.g., 50): ").strip())
        except ValueError:
            print("\033[31mInvalid token number. Please try model selection again.\033[0m")
            continue

        while True:
            user_input = input("\033[92mEnter text to process (or 'change' to change model, 'exit' to quit): \033[0m").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("\033[31mExiting program.\033[0m")
                return  # Exit entire program
            elif user_input.lower() == "change":
                # User wants to change the model; re-display the models table
                display_models(models)
                break  # Break inner loop to choose a new model
            
            processed_response, raw_api_data = query_model(selected_model['model_id'], user_input, max_tokens)
            print("\033[96mModel Response:\033[33m", processed_response)
            print("\033[34mRaw API Data:\033[94m", raw_api_data)

if __name__ == "__main__":
    main()
