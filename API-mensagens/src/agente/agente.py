from pymongo import MongoClient
from src.agente.ia_service import gerar_resposta
import os
from dotenv import load_dotenv

load_dotenv()

def processar_mensagem(mensagem, nome):

    connection_string = os.getenv("MONGODB_URL")
    database_name = os.getenv("DATABASE_NAME")
 
    # Conectar ao banco
    cliente = MongoClient(connection_string)

    
    db = cliente[database_name]


    collection = db["mensagens"]

    # Contar mensagens desse usuário
    quantidade = collection.count_documents({
        "user": nome
        #"$or": [
         #   {"from": nome},
          #  {"to": nome}
        #]
    })

    # Decidir resposta
    if quantidade == 1:
        return f"Oi {nome}, como posso te ajudar?"
    
    else: 
         resposta = gerar_resposta(mensagem)
         print("RESPOSTA DO BOT:", resposta)
         return resposta
         



def responder_bot(mensagem):

    resposta = gerar_resposta(mensagem["text"])

    return {
        "from": "bot",
        "to": mensagem["from"],
        "text": resposta
    }
    

    
#if __name__ == "__main__":
 #   resposta = processar_mensagem("oi", "Laerte")
  #  print(resposta)


    
    
   