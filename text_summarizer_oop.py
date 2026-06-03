import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TextSummarizer:
    """Summarize text using AI"""
    
    def __init__(self):
        """Initialize with API key"""
        self.api_key = os.getenv("OPENROUTER_KEY")
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
    
    def summarize(self, text, sentences):
        """Summarize text into specified number of sentences"""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if not sentences or int(sentences) < 1:
            raise ValueError("Sentences must be at least 1")
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + self.api_key},
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Summarize this text in {sentences} clear sentences: {text}"
                        }
                    ]
                }
            )
            
            data = response.json()
            
            if "error" in data:
                return f"Error: {data['error']['message']}"
            
            return data["choices"][0]["message"]["content"]
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_summary(self, summary, filename):
        """Save summary to file"""
        try:
            with open(filename + ".txt", "w", encoding="utf-8") as f:
                f.write(summary)
            return f"Saved to {filename}.txt"
        except Exception as e:
            return f"Error saving: {str(e)}"

# Main program with user input
print("=== AI Text Summarizer ===\n")

summarizer = TextSummarizer()

# Option 1: Type text
text = input("Enter text to summarize (or 'file' to read from file): ").strip()

if text.lower() == "file":
    filename = input("Enter filename: ")
    try:
        with open(filename, "r", encoding="latin-1") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        exit()

sentences = input("How many sentences for summary? ")

print("\nSummarizing...")
summary = summarizer.summarize(text, sentences)

print(f"\n--- Summary ---")
print(summary)

save = input("\nSave summary? (yes/no): ")
if save.lower() == "yes":
    filename = input("Filename (without .txt): ")
    result = summarizer.save_summary(summary, filename)
    print(result)