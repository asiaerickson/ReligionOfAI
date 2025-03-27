import os
from openai import OpenAI

# Create OpenAI client
client = OpenAI(
    api_key='API_KEY'
)

def chat_with_gpt4(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are a helpful chatbot."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini", temperature = 0.5 , max_tokens = 1000
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("Welcome to GPT-4o-mini Chat!")
    while True:
        user_input = input("\nEnter your message (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_with_gpt4(user_input)
        print("\nGPT-4o-mini Response:")
        print(response)
