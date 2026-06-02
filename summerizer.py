import requests

def summarize(text, sentences):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer YOUR_OPENROUTER_KEY_HERE"
        },
        json={
            "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
            "messages": [
                {
                    "role": "user",
                    "content": "Summarize this text in " + sentences + " sentences: " + text
                }
            ]
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]

file_input = open("C:\\Users\\LAH\\Desktop\\input_text.txt", "r", encoding="latin-1")
text = file_input.read()
file_input.close()

sentences = input("How many sentences for the summary? ")
summary = summarize(text, sentences)

print("\n--- SUMMARY ---")
print(summary)

filename = input("What should we name the summary file? ")
file = open(filename + ".txt", "w", encoding="utf-8")
file.write(summary)
file.close()

print("\nSummary saved to " + filename + ".txt")