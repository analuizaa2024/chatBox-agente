import requests

API_KEY = "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"

def gerar_resposta(pergunta):
   

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": pergunta
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    

    data = response.json()
    print("RESPOSTA DA API:")
    print(data)

    return data["choices"][0]["message"]["content"]
