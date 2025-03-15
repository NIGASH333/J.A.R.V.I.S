import requests

def query_deepseek(prompt):
    url = "http://localhost:11434/api/generate"  # Change this if Ollama runs on a different port
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        return response_json.get("response", "I couldn't understand that.")
    except Exception as e:
        return f"Error communicating with DeepSeek: {str(e)}"
