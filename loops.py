import json
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

def generate_scenarios(initial_prompt, num_scenarios=5):
    """Generates multiple scenarios from an initial prompt."""
    #scenario_prompt = f"Generate {num_scenarios} different scenarios based on the following input: {initial_prompt}"
    scenario_prompt = f"{initial_prompt}"
    scenarios_text = chat_with_gpt4(scenario_prompt)
    scenarios = scenarios_text.split("\n")  # Assuming GPT returns a list-like response
    return [s.strip() for s in scenarios if s.strip()], scenario_prompt  # Return cleaned scenarios and the actual prompt used

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Step 1: Generate scenarios
    scenario_prompt = input("Enter a prompt to generate scenarios: ")
    scenarios, generated_scenario_prompt = generate_scenarios(scenario_prompt)

    # Save scenarios to JSON with the prompt used
    scenario_data = {
        "scenario_prompt": scenario_prompt,
        "generated_scenario_prompt": generated_scenario_prompt,
        "scenarios": scenarios
    }
    save_to_json(scenario_data, "scenarios3.json")
    print("Scenarios saved to scenarios3.json!")

    # Step 2: Generate responses
    response_prompt = input("Enter a prompt for generating responses to the scenarios: ")
    responses_data = {
        "scenario_prompt": scenario_prompt,
        "response_prompt": response_prompt,
        "responses": []
    }

    for scenario in scenarios:
        response_1 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")
        response_2 = chat_with_gpt4(f"{response_prompt} Scenario: {scenario}")

        responses_data["responses"].append({
            "scenario": scenario,
            "responses": [response_1, response_2]
        })

    # Save responses to JSON with prompts used
    save_to_json(responses_data, "responses3.json")
    print("Responses saved to responses3.json!")
