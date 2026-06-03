class AIAssistant:
    """A simple AI assistant class"""

    def __init__(self, name):
        """Initialize with a name"""
        self.name = name
        self.conversation_history = []
    
    def add_message(self, role, content):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_history(self):
        """Return the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []

    def count_messages(self):
        """Count total messages in the conversation history"""
        return len(self.conversation_history)
# Test the AIAssistant class
assistant = AIAssistant("Claude")
assistant.add_message("user", "Hello!")
assistant.add_message("assistant", "Hi there!")
print(f"Total Messages: {assistant.count_messages()}")
print(f"History: {assistant.get_history()}")