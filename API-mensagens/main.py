import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.server.instance import server  # tras o instance para o main
import src.server.mensagens

if __name__ == '__main__':
    server.app.run(host="0.0.0.0", port=5000, debug=True)  #“Se este arquivo está sendo executado diretamente, então inicie o servidor da API.”