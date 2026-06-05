import requests
import json
import os
from dotenv import load_dotenv
from database_handler import Database

load_dotenv()

class ChatApplicationWithDatabase:
    """Chat app with permanent data storage"""
    
    def __init__(self, user_id="default_user"):
        self.api_key = os.getenv("OPENROUTER_KEY")
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
        self.user_id = user_id
        self.db = Database("chat_history.db")
        self.db.create_conversations_table()
        self.conversation = []
    
    def send_message(self, user_input):
        """Send message and save to database"""
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
                },
                timeout=60
            )
            
            data = response.json()
            
            if "error" in data:
                return f"Error: {data['error']['message']}"
            
            ai_response = data["choices"][0]["message"]["content"]
            self.conversation.append({"role": "assistant", "content": ai_response})
            
            # Save to database
            self.db.insert_conversation(user_input, ai_response, self.user_id)
            
            return ai_response
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def load_conversation_history(self):
        """Load previous conversations from database"""
        conversations = self.db.get_all_conversations(self.user_id)
        self.conversation = []
        for conv in conversations:
            self.conversation.append({"role": "user", "content": conv[1]})
            self.conversation.append({"role": "assistant", "content": conv[2]})
        return len(conversations)
    
    def get_conversation_count(self):
        """Get total conversations stored"""
        conversations = self.db.get_all_conversations(self.user_id)
        return len(conversations)
    
    def close(self):
        """Close database"""
        self.db.close()

# Main program
print("=== AI Chat with Database ===")
print("Your conversations are now saved permanently!\n")

user_id = input("Enter your name (or press Enter for default): ").strip() or "default_user"
chat = ChatApplicationWithDatabase(user_id=user_id)

# Load previous conversations
count = chat.load_conversation_history()
if count > 0:
    print(f"Loaded {count} previous conversations from database.\n")
else:
    print("Starting new conversation.\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        chat.close()
        break
    
    elif user_input.lower() == "count":
        count = chat.get_conversation_count()
        print(f"Total conversations stored: {count}\n")
        continue
    
    if not user_input:
        continue
    
    print("AI thinking...")
    response = chat.send_message(user_input)
    print(f"AI: {response}\n")
