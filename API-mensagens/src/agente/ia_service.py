import os
import requests

API_KEY = os.getenv("API_KEY")

API_URL = "https://router.huggingface.co/hf-inference/models/gpt2"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def gerar_resposta(pergunta):

    payload = {
        "inputs": pergunta,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    data = response.json()

    print(data)  # <-- para ver o que a API está retornando

    if isinstance(data, list):
        return data[0]["generated_text"]
    else:
        return "Erro ao gerar resposta da IA"
