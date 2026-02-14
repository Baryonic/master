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

# API endpoints and headers
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_LIST_URL = "https://openrouter.ai/api/v1/models"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_free_models():
    """
    Fetch available models from the API, filter for free models, and return
    a dictionary of free models keyed by a numeric index.
    
    Each model dictionary contains:
      - model_id: the unique model identifier
      - name: the name of the model (if available)
      - context_length: maximum context length
    """
    try:
        response = requests.get(MODEL_LIST_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        models = {}
        free_model_count = 0

        if not data or not isinstance(data.get("data", []), list):
            print("\033[31mNo models available or invalid API response.\033[0m")
            return {}

        for item in data.get("data", []):
            model_id = item.get("id", "Unknown ID")
            name = item.get("name", model_id)  # Fallback to model_id if name is missing
            context_length = item.get("context_length", "Unknown")
            pricing = item.get("pricing", {})
            prompt_cost = pricing.get("prompt")
            completion_cost = pricing.get("completion")

            # Convert pricing values to float for proper comparison.
            try:
                prompt_cost_val = float(prompt_cost) if prompt_cost is not None else None
                completion_cost_val = float(completion_cost) if completion_cost is not None else None
            except (TypeError, ValueError):
                continue  # Skip models with uninterpretable pricing

            # A free model: either explicitly tagged as free or both costs equal to 0.
            if model_id.endswith(":free") or (prompt_cost_val == 0 and completion_cost_val == 0):
                free_model_count += 1
                models[free_model_count] = {
                    "model_id": model_id,
                    "name": name,
                    "context_length": context_length,
                    "pricing": pricing  # Optional for troubleshooting
                }
        return models

    except requests.exceptions.RequestException as e:
        print(f"\033[31mError: {type(e).__name__} - {e}\033[0m")
        return {}

def display_models(models):
    """Display free models in a formatted table with numeric ID, name, context length, and model ID."""
    print("\n\033[92mAvailable Free Models:\033[0m\n")
    if not models:
        print("\033[31mNo free models loaded.\033[0m")
        return

    header = f"{'ID':<5} {'Name':<50} {'Context Length':<20} {'Model ID':<40}"
    print(header)
    print("-" * len(header))
    for num, details in models.items():
        print(f"{num:<5} {details['name']:<50} {details['context_length']:<20} {details['model_id']:<40}")

def query_model(model_id, user_input, max_tokens):
    """
    Send a query to the OpenRouter API using the specified free model.
    Returns a tuple of (processed_response, raw_api_data).
    """
    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": model_id,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data and "choices" in data:
            choices = data.get("choices", [])
            if choices and isinstance(choices, list):
                processed_response = choices[0].get("message", {}).get("content", "No response.")
            else:
                processed_response = "\033[31mError: Invalid API structure.\033[0m"
        else:
            processed_response = "\033[31mError: No valid response received.\033[0m"

        return processed_response, data
        
    except requests.exceptions.RequestException as e:
        return f"\033[31mAPI Request Error: {e}\033[0m", {}

def main():
    models = load_free_models()
    if not models:
        print("\033[31mNo free models available. Exiting.\033[0m")
        return

    display_models(models)

    while True:
        choice = input("\033[93mSelect a model number (or 'exit' to quit): \033[0m").strip()
        if choice.lower() in ["exit", "quit"]:
            print("\033[31mExiting program.\033[0m")
            break
        if not choice.isdigit() or int(choice) not in models:
            print("\033[31mInvalid choice. Please enter a valid numeric ID.\033[0m")
            continue

        selected_model = models[int(choice)]
        print(f"\nUsing model: \033[93m{selected_model['name']} ({selected_model['model_id']})\033[0m with context length: {selected_model['context_length']}")
        try:
            max_tokens = int(input("Enter max tokens for completion (e.g., 50): ").strip())
        except ValueError:
            print("\033[31mInvalid token number. Restarting model selection.\033[0m")
            continue

        while True:
            user_input = input("\033[92mEnter text to process (or 'change' to select a different model, 'exit' to quit): \033[0m").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("\033[31mExiting program.\033[0m")
                return
            elif user_input.lower() == "change":
                display_models(models)
                break  # Break inner loop for model selection

            processed_response, raw_data = query_model(selected_model['model_id'], user_input, max_tokens)
            print("\033[96mModel Response:\033[33m", processed_response)
            print("\033[34mRaw API Data:\033[94m", raw_data)
            
            # New functionality: Print token usage details if available.
            if raw_data and 'usage' in raw_data:
                usage = raw_data['usage']
                prompt_tokens = usage.get('prompt_tokens', 'N/A')
                completion_tokens = usage.get('completion_tokens', 'N/A')
                total_tokens = usage.get('total_tokens', 'N/A')
                print(f"\033[95mToken Usage: Prompt Tokens: {prompt_tokens} | Completion Tokens: {completion_tokens} | Total Tokens: {total_tokens}\033[0m")

if __name__ == "__main__":
    main()
