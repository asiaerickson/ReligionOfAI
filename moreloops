#Looped Responses: It now processes one scenario per loop iteration instead of generating all responses at once.
#Incremental JSON Storage: The responses are stored in a JSON file, appending new responses as they are generated.

import json
import os
from openai import OpenAI

# Create OpenAI client
client = OpenAI(api_key="API_KEY")

def chat_with_gpt4(prompt):
    """Function to get a response from GPT-4o-mini."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini", temperature=0.7, max_tokens=1000
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def generate_scenarios(initial_prompt):
    """Generates multiple scenarios from an initial prompt."""
    scenarios_text = chat_with_gpt4(initial_prompt)
    scenarios = scenarios_text.split("\n")  # Assuming GPT returns a list-like response
    return [s.strip() for s in scenarios if s.strip()], initial_prompt  # Return cleaned scenarios and the actual prompt used

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_from_json(filename):
    """Loads data from a JSON file if it exists, otherwise returns an empty list."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    # Step 1: Generate scenarios
    scenario_prompt = input("Enter a prompt to generate scenarios: ")
    scenarios, generated_scenario_prompt = generate_scenarios(scenario_prompt)

    # Save scenarios to JSON
    scenario_data = {
        "scenario_prompt": scenario_prompt,
        "generated_scenario_prompt": generated_scenario_prompt,
        "scenarios": scenarios
    }
    save_to_json(scenario_data, "scenarios4.json")
    print("Scenarios saved to scenarios4.json!")

    # Step 2: Generate responses incrementally
    response_prompt = input("Enter a prompt for generating responses to the scenarios: ")

    responses_data = load_from_json("responses4.json")
    responses_data.setdefault("scenario_prompt", scenario_prompt)
    responses_data.setdefault("response_prompt", response_prompt)
    responses_data.setdefault("responses", [])

    for scenario in scenarios:
        print(f"\nProcessing scenario: {scenario}")

        # Generate two responses for the scenario
        response_1 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")
        response_2 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")

        responses_data["responses"].append({
            "scenario": scenario,
            "responses": [response_1, response_2]  # Store two responses per scenario
        })

        # Save after each iteration to ensure progress isn't lost
        save_to_json(responses_data, "responses4.json")
        print(f"Responses saved for scenario: {scenario}")

    print("All responses saved to response4s.json!")

