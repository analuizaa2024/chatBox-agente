from pymongo import MongoClient

def processar_mensagem(mensagem, nome):
 
    # Conectar ao banco
    cliente = MongoClient("mongodb+srv://AnaLuiza:AnaLuiza@cluster0.elo3l5s.mongodb.net/?appName=Cluster0")
    db = cliente["ChatBot"]
    collection = db["mensagens"]

    # Contar mensagens desse usuário
    quantidade = collection.count_documents({
        "$or": [
            {"user": nome},
            {"to": nome}
        ]
    })

    # Decidir resposta
    if quantidade == 0:
        return f"Oi {nome}, como posso te ajudar?"
    else:
        return "Ainda estou aprendendo, mas vou tentar te ajudar!"
    

    
if __name__ == "__main__":
    resposta = processar_mensagem("oi", "Ana")
    print(resposta)
    
    
   