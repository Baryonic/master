#!/usr/bin/env python3
import os
import base64
import requests  # type: ignore
from datetime import datetime
import sys

sys.path.append(os.path.join(os.path.expanduser("~"), "master", "libs"))
try:
    import secrets_manager
except ImportError:
    print("Error: Could not import secrets_manager.")
    sys.exit(1)

API_KEY = secrets_manager.get_secret("open_router.key")

# API endpoints and headers
API_URL = "https://openrouter.ai/api/v1/chat/completions"  # same endpoint for both text and multimodal analysis
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
            name = item.get("name", model_id)  # fallback if name is missing
            context_length = item.get("context_length", "Unknown")
            pricing = item.get("pricing", {})
            prompt_cost = pricing.get("prompt")
            completion_cost = pricing.get("completion")

            try:
                prompt_cost_val = float(prompt_cost) if prompt_cost is not None else None
                completion_cost_val = float(completion_cost) if completion_cost is not None else None
            except (TypeError, ValueError):
                continue

            # A free model is either explicitly tagged as free or has zero prompt and completion costs.
            if model_id.endswith(":free") or (prompt_cost_val == 0 and completion_cost_val == 0):
                free_model_count += 1
                models[free_model_count] = {
                    "model_id": model_id,
                    "name": name,
                    "context_length": context_length,
                    "pricing": pricing
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

def query_text_model(model_id, user_input, max_tokens):
    """
    Send a text prompt to the OpenRouter API via the chat completions endpoint.
    Returns a tuple (processed_response, raw_api_data).
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

def query_multimodal_model(model_id, text_prompt, image_path, max_tokens):
    """
    Send a multimodal request to the OpenRouter API using the given text prompt and image.
    The image from the specified file is base64‑encoded and attached as a second message.

    The API is expected to return its analysis (in text) in the first choice’s message.

    Returns a tuple (processed_response, raw_api_data).
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        return f"\033[31mError reading image file: {e}\033[0m", {}

    payload = {
        "messages": [
            {"role": "user", "content": text_prompt},
            {"role": "user", "image": encoded_image}
        ],
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
                processed_response = choices[0].get("message", {}).get("content", "No analysis returned.")
            else:
                processed_response = "\033[31mError: Invalid API response structure.\033[0m"
        else:
            processed_response = "\033[31mError: No valid response received from API.\033[0m"
        return processed_response, data

    except requests.exceptions.RequestException as e:
        return f"\033[31mAPI Request Error: {e}\033[0m", {}

def parse_max_tokens(token_input, context_length):
    """
    Parse the user's max tokens input. The user can provide:
      - An absolute number (e.g., 150) if greater than 100
      - A percentage (e.g., 67 or 67%) if the value is less than or equal to 100
    When a percentage is given, the limit is computed as (context_length * percentage/100).
    Returns the computed max_tokens as an integer, or None if parsing fails.
    """
    token_input = token_input.strip()
    try:
        # Remove the % symbol, if present.
        value = int(token_input.rstrip("%"))
        # If the value is <= 100, treat it as a percentage.
        if value <= 100:
            computed = int(int(context_length) * value / 100)
            print(f"\033[92mInterpreting input as percentage: {value}% of {context_length} => {computed} tokens\033[0m")
            return computed
        else:
            # Otherwise, assume it's an absolute token count.
            return value
    except ValueError:
        print("\033[31mInvalid token input. Please enter a number or a percentage (e.g., 67 or 67%).\033[0m")
        return None

def list_images(directory="img"):
    """
    List image files from the given directory, filtering for common image file extensions.
    Returns a list of image file names.
    """
    if not os.path.isdir(directory):
        return []
    files = os.listdir(directory)
    image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
    return image_files

def select_image(directory="img"):
    """
    List the images in the given directory and prompt the user to select one by its number.
    Returns the full path to the selected image.
    """
    images = list_images(directory)
    if not images:
        print(f"\033[31mNo images found in the '{directory}' folder.\033[0m")
        image_path = input("Enter the image file path manually: ").strip()
        return image_path
    print("\n\033[92mAvailable Images:\033[0m")
    for idx, image in enumerate(images, start=1):
        print(f"{idx}: {image}")
    while True:
        choice = input("Select an image by number (or enter 0 to type a custom path): ").strip()
        if choice.isdigit():
            num = int(choice)
            if num == 0:
                image_path = input("Enter the image file path: ").strip()
                if os.path.isfile(image_path):
                    return image_path
                else:
                    print("\033[31mFile does not exist. Please try again.\033[0m")
            elif 1 <= num <= len(images):
                return os.path.join(directory, images[num - 1])
            else:
                print("\033[31mInvalid number. Please select from the list above.\033[0m")
        else:
            print("\033[31mInvalid input. Please enter a number.\033[0m")

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
        print(f"\nUsing model: \033[93m{selected_model['name']} ({selected_model['model_id']})\033[0m "
              f"with context length: {selected_model['context_length']}")

        while True:
            mode = input("\033[92mSelect mode ('text' or 'image', or 'change' to select a different model, 'exit' to quit): \033[0m").strip().lower()
            if mode in ["exit", "quit"]:
                print("\033[31mExiting program.\033[0m")
                return
            elif mode == "change":
                display_models(models)
                break  # Back to model selection
            elif mode not in ["text", "image"]:
                print("\033[31mInvalid mode selection. Please enter 'text' or 'image'.\033[0m")
                continue

            # Ask for max tokens using an absolute number or percentage.
            max_tokens_input = input("Enter max tokens for completion (e.g., 150 or 50 for 50%): ").strip()
            max_tokens = parse_max_tokens(max_tokens_input, selected_model["context_length"])
            if max_tokens is None:
                continue

            # Process prompts for the chosen mode.
            while True:
                if mode == "text":
                    user_prompt = input("\033[92mEnter text to process (or 'change' to select a different model, 'exit' to quit): \033[0m").strip()
                    if user_prompt.lower() in ["exit", "quit"]:
                        print("\033[31mExiting program.\033[0m")
                        return
                    elif user_prompt.lower() == "change":
                        display_models(models)
                        break  # Back to model/mode selection

                    processed_response, raw_data = query_text_model(selected_model["model_id"], user_prompt, max_tokens)
                    print("\033[96mModel Response:\033[33m", processed_response)
                    print("\033[34mRaw API Data:\033[94m", raw_data)
                    if raw_data.get("usage"):
                        usage = raw_data["usage"]
                        print(f"\033[95mToken Usage: Prompt Tokens: {usage.get('prompt_tokens', 'N/A')} | "
                              f"Completion Tokens: {usage.get('completion_tokens', 'N/A')} | Total Tokens: {usage.get('total_tokens', 'N/A')}\033[0m")
                else:  # mode == "image" (multimodal analysis)
                    user_prompt = input("\033[92mEnter prompt for image analysis (or 'change' to select a different model, 'exit' to quit): \033[0m").strip()
                    if user_prompt.lower() in ["exit", "quit"]:
                        print("\033[31mExiting program.\033[0m")
                        return
                    elif user_prompt.lower() == "change":
                        display_models(models)
                        break  # Back to model/mode selection

                    # Let the user choose an image from the img/ folder.
                    image_path = select_image("img")
                    if not os.path.isfile(image_path):
                        print("\033[31mError: File does not exist. Please try again.\033[0m")
                        continue

                    processed_response, raw_data = query_multimodal_model(
                        selected_model["model_id"], user_prompt, image_path, max_tokens
                    )
                    print("\033[96mModel Analysis Response:\033[33m", processed_response)
                    print("\033[34mRaw API Data:\033[94m", raw_data)
                    
if __name__ == "__main__":
    main()