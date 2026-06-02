import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def chat_with_ai(conversation_history):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}"
            },
            json={"model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": conversation_history}
        )
        data = response.json()
        if "error" in data:
            return f"Error: {data['error']['message']}"
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Connection error occurred: {str(e)}"
def save_conversation(conversation_history, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(conversation_history, file, indent=2)
        print(f"\nSaved to {filename}")
    except Exception as e:
        print(f"Error: {str(e)}")

print( "=== AI Chat ===")
conversation= []

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break
    if user_input.lower() == "save":
        filename = input("Filename: ")
        save_conversation(conversation, filename + ".json")
        continue
    if not user_input:
        continue
    conversation.append({"role": "user", "content": user_input})
    ai_response = chat_with_ai(conversation)
    print(f"AI: {ai_response}\n")
    conversation.append({"role": "assistant", "content": ai_response})