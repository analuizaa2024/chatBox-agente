import requests

API_KEY = "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"

def gerar_resposta(pergunta):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": pergunta
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    return data["choices"][0]["message"]["content"]
