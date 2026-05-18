import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
def gerar_resposta(pergunta):
   

    url = os.getenv("OPENROUTER_URL")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("API_KEY carregada?", API_KEY is not None)
    print("URL:", url)

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

    if "choices" not in data:
        return f"Erro na API: {data}"

    return data["choices"][0]["message"]["content"]
