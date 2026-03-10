from flask import Flask
from flask_restx import Api, Namespace

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        # Configuração da API
        self.api = Api(
            self.app,
            version='1.0',
            title='API de mensagens',
            description='Uma API simples para enviar e gerenciar mensagens.',
            doc='/docs'  # rota do Swagger
        )

        # Namespace para agrupar rotas relacionadas
        self.ns_mensagens = Namespace('mensagens', description='Operações relacionadas a mensagens')
        self.api.add_namespace(self.ns_mensagens)

        # TRATAMENTO GLOBAL DE ERROS
        @self.api.errorhandler
        def default_error_handler(error):
            """
            Esse método captura QUALQUER erro que não foi tratado
            e retorna em formato JSON bonito no Swagger.
            """
            code = getattr(error, 'code', 500)
            return {
                "status": "error",
                "message": str(error)
            }, code

    def run(self):
        """Executa o servidor Flask"""
        self.app.run(debug=True)

# Instância global do servidor
server = Server()
