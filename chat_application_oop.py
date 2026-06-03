import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ChatApplication:
    """Multi-turn AI chat with conversation memory"""
    
    def __init__(self):
        """Initialize chat app"""
        self.api_key = os.getenv("OPENROUTER_KEY")
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
        self.conversation = []
    
    def send_message(self, user_input):
        """Send message and get response"""
        if not user_input or not user_input.strip():
            return "Please enter a message"
        
        self.conversation.append({"role": "user", "content": user_input})
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + self.api_key},
                json={
                    "model": self.model,
                    "messages": self.conversation
                }
            )
            
            data = response.json()
            
            if "error" in data:
                return f"Error: {data['error']['message']}"
            
            ai_response = data["choices"][0]["message"]["content"]
            self.conversation.append({"role": "assistant", "content": ai_response})
            return ai_response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_conversation(self, filename):
        """Save conversation to JSON file"""
        try:
            with open(filename + ".json", "w", encoding="utf-8") as f:
                json.dump(self.conversation, f, indent=2)
            return f"Saved to {filename}.json"
        except Exception as e:
            return f"Error saving: {str(e)}"
    
    def get_conversation_count(self):
        """Get total messages in conversation"""
        return len(self.conversation)
    
    def clear_conversation(self):
        """Clear all messages"""
        self.conversation = []
        return "Conversation cleared"

# Main program
print("=== AI Chat Application ===")
print("Commands: 'save', 'clear', 'count', 'quit'\n")

chat = ChatApplication()

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    elif user_input.lower() == "save":
        filename = input("Filename (without .json): ")
        result = chat.save_conversation(filename)
        print(result)
        continue
    
    elif user_input.lower() == "clear":
        result = chat.clear_conversation()
        print(result)
        continue
    
    elif user_input.lower() == "count":
        count = chat.get_conversation_count()
        print(f"Total messages: {count}")
        continue
    
    if not user_input:
        print("Please enter something.\n")
        continue
    
    print("\nAI thinking...")
    response = chat.send_message(user_input)
    print(f"AI: {response}\n")