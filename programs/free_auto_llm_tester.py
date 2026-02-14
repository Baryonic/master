# New Python file

import requests #type: ignore
import datetime
import csv
#from configs import API_KEY
import concurrent.futures
import os

# API endpoints and headers
API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_LIST_URL = "https://openrouter.ai/api/v1/models"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_free_models():
    """
    Fetch available models from the API, filtering only for free models where pricing is 0.
    Returns a dictionary keyed by model IDs containing model name and context length.
    """
    try:
        response = requests.get(MODEL_LIST_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        free_models = {}
        if not data or not isinstance(data.get("data", []), list):
            print("No models available or invalid API response.")
            return {}

        for item in data.get("data", []):
            model_id = item.get("id", "Unknown ID")
            name = item.get("name", model_id)
            context_length = item.get("context_length", 100)  # default if missing
            pricing = item.get("pricing", {})
            prompt_cost = pricing.get("prompt")
            completion_cost = pricing.get("completion")

            # Convert pricing values to float for proper comparison.
            try:
                prompt_cost_val = float(prompt_cost) if prompt_cost is not None else None
                completion_cost_val = float(completion_cost) if completion_cost is not None else None
            except (TypeError, ValueError):
                continue

            if model_id.endswith(":free") or (prompt_cost_val == 0 and completion_cost_val == 0):
                free_models[model_id] = {
                    "name": name,
                    "context_length": context_length
                }
        return free_models

    except requests.exceptions.RequestException as e:
        print(f"Error: {type(e).__name__} - {e}")
        return {}

def query_model(model_id, prompt, max_tokens):
    """
    Sends a query to the OpenRouter API for the given model using the provided prompt and max_tokens.
    Returns a tuple containing the processed response text and the raw response data.
    """
    print(f"\033[94mquery payload to \033[92m{model_id},\033[94m max_tokens=\033[92m{max_tokens}")
    payload = {
        "messages": [{  
            "role": "user",
            #"content": f"{prompt}. format: shortest answer,. instructions: don't repeat yourself."
            #"content": f"{prompt}. format: shortest answer,. instructions: don't repeat yourself, use as least tokens as posible."
            #"content": f"{prompt}"
            "content":f"{prompt}. don't repeat yourself"
        }],
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
                processed_response = "Error: Invalid API structure."
        else:
            processed_response = "Error: No valid response received."
        return processed_response, data

    except requests.exceptions.RequestException as e:
        return f"API Request Error: {e}", {}

def create_html_report_for_prompt(prompt):
    """
    Loads all free models, sends the same prompt (provided as a parameter) to each model with
    max_tokens set to 50% of its context length, and creates an HTML file that contains an <h1>
    with the prompt text and a table showing (1) the model name, (2) tokens used, and (3) the model's reply.
    
    The produced HTML file links to the external stylesheet 'estilo.css'.
    """
    free_models = load_free_models()
    if not free_models:
        print("No free models available. Exiting.")
        return None

    results = []
    # Prepare arguments for parallel execution
    model_args = []
    for model_id, details in free_models.items():
        try:
            max_tokens = int(details["context_length"] // 2)
        except Exception:
            max_tokens = 50  # Fallback value
        model_args.append((model_id, details, max_tokens))

    def query_wrapper(args):
        model_id, details, max_tokens = args
        response_text, raw_data = query_model(model_id, prompt, max_tokens)
        tokens = "N/A"
        if raw_data and "usage" in raw_data:
            tokens = raw_data["usage"].get("total_tokens", "N/A")
        return {
            "model_name": details["name"],
            "tokens": tokens,
            "response": response_text
        }

    # Use ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_model = {executor.submit(query_wrapper, args): args for args in model_args}
        for future in concurrent.futures.as_completed(future_to_model):
            result = future.result()
            results.append(result)

    # Create a unique filename using a timestamp and a safe version of the prompt text.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_")[:20]
    filename = f"{safe_prompt}_{timestamp}.html"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Model Comparison Report</title>
    <link rel="stylesheet" href="estilo.css" media="all">
</head>
<body>
    <h1>{prompt}</h1>
    <table>
        <thead>
            <tr>
                <th>Model Name</th>
                <th>Tokens Used</th>
                <th>Response</th>
            </tr>
        </thead>
        <tbody>
    """

    for result in results:
        model_name = result["model_name"]
        tokens = result["tokens"]
        # Replace newlines in the response with <br> for better HTML formatting.
        response_formatted = result["response"].replace("\n", "<br>")
        html_content += f"""<tr>
            <td>{model_name}</td>
            <td>{tokens}</td>
            <td>{response_formatted}</td>
        </tr>
        """

    html_content += """
        </tbody>
    </table>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML report saved as '{filename}'.")
    return filename

def process_pending_questions():
    """
    Reads pending questions from 'preguntas_pendientes.csv'. For each pending question, it:
    - Creates an HTML file report,
    - Appends the question to 'preguntas_resueltas.csv', and
    - Removes the processed question from 'preguntas_pendientes.csv'.
    
    It notifies the user each time an HTML file is created.
    """
    print("processing questions in 'preguntas_pendientes.csv'")
    pending_file = "preguntas_pendientes.csv"
    resolved_file = "preguntas_resueltas.csv"

    try:
        with open(pending_file, "r", encoding="utf-8") as pf:
            pending_lines = pf.readlines()
    except FileNotFoundError:
        print(f"File {pending_file} not found.")
        return

    # Remove blank lines and strip newline characters.
    pending_questions = [line.strip() for line in pending_lines if line.strip()]

    if not pending_questions:
        try:
            new_question = input("\033[31mNo pending questions found. \033[92mPlease enter a new question for the models (or type 'exit' to quit):\033[0m ").strip()
            if new_question.lower() in ('exit', 'quit'):
                print("Exiting as requested by the user.")
                return
            if new_question:
                pending_questions = [new_question]
            else:
                print("No question provided. Exiting.")
                return
        except (KeyboardInterrupt, EOFError):
            print("\nExiting as requested by the user.")
            return

    # List for questions that still remain pending (if any)
    remaining_questions = []

    for question in pending_questions:
        # Create HTML report for the given question
        if question:
            print(f"\033[94mprocessing question: \033[94m{question}. \033[31mPlease dont stop the program")
            create_html_report_for_prompt(question)
            # Append the processed question to the resolved file.
            with open(resolved_file, "a", encoding="utf-8") as rf:
                rf.write(question + "\n")
            # Notify the user that this question has been processed.
            print(f"\033[92m Processed question: \033[0m{question}")
        else:
            remaining_questions.append(question)

    # After processing, overwrite the pending file with any remaining questions.
    with open(pending_file, "w", encoding="utf-8") as pf:
        for q in remaining_questions:
            pf.write(q + "\n")

if __name__ == "__main__":
    print("\033[94mrunning FREE AUTO TESTER HTML 3 (fath3.py)")
    process_pending_questions()