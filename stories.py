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

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_from_json(filename):
    """Loads data from a JSON file if it exists, otherwise returns an empty dictionary."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Step 1: Generate Scenarios
scenario_prompt = input("Enter a prompt to generate scenarios: ")
scenarios_text = chat_with_gpt4(scenario_prompt)
scenarios = [s.strip() for s in scenarios_text.split("\n") if s.strip()]

scenario_data = {
    "scenario_prompt": scenario_prompt,
    "scenarios": scenarios
}
save_to_json(scenario_data, "1scenarios.json")
print("Scenarios saved to 1scenarios.json!")

# Step 2: Generate Responses
response_prompt = input("Enter a prompt for generating responses to the scenarios: ")

responses_data = load_from_json("1responses.json")
responses_data.setdefault("scenario_prompt", scenario_prompt)
responses_data.setdefault("response_prompt", response_prompt)
responses_data.setdefault("responses", [])

for scenario in scenarios:
    print(f"\nProcessing scenario: {scenario}")

    response_1 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")
    response_2 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")

    responses_data["responses"].append({
        "scenario": scenario,
        "responses": [response_1, response_2]
    })

    save_to_json(responses_data, "1responses.json")
    print(f"Responses saved for scenario: {scenario}")

print("All responses saved to 1responses.json!")

# Step 3: Generate Parables
parable_prompt = input("Enter a prompt for generating parables: ")

paragraphs_data = load_from_json("1paragraphs.json")
paragraphs_data.setdefault("paragraphs", [])

for entry in responses_data["responses"]:
    scenario = entry["scenario"]
    response_1, response_2 = entry["responses"]

    print(f"\nGenerating parable for scenario: {scenario}")

    # Use the exact parable prompt given by the user
    parable_input = f"{parable_prompt}\nScenario: {scenario}\nResponse 1: {response_1}\nResponse 2: {response_2}"
    parable = chat_with_gpt4(parable_input)

    paragraphs_data["paragraphs"].append({
        "scenario": scenario,
        "responses": [response_1, response_2],
        "parable": parable
    })

    save_to_json(paragraphs_data, "1paragraphs.json")
    print(f"Parable saved for scenario: {scenario}")

print("All parables saved to 1paragraphs.json!")
