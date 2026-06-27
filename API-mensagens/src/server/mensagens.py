from flask import request
from flask_restx import reqparse, abort, Resource, fields
from src.server.instance import server
from src.server.raw import collection, users_collection
from bson import ObjectId
from flask_cors import CORS
from src.agente.agente import processar_mensagem
print("MENSAGENS IMPORTADO")

# Ativar CORS
CORS(server.app)

# Acessar namespace e api criados no instance.py
ns = server.ns_mensagens
ns_users = server.api.namespace('users', description='Operações de usuários')
api = server.api

# MODELOS DO SWAGGER

# Modelo padrão para mensagens
mensagem_model = ns.model('Mensagem', {
    'user': fields.String(required=True, description='Nome do usuário que envia a mensagem'),
    'msg': fields.String(required=True, description='Conteúdo da mensagem'),
    'to': fields.String(required=True, description='Destinatário'),
    'id': fields.String(description='ID da mensagem no banco')
})

usuario_model = ns_users.model('Usuario', {
    'name': fields.String(required=True, description = 'Nome do usuário'),
    'email': fields.String(required=True, description = 'Email do usuário'),
    'photo': fields.String(required=True, description = 'Foto do usuário'),
    'role': fields.String(required=True, description = 'Cargo do usuário'),
    'password': fields.String(required=True, description = 'Senha do usuário'),
})

# Modelo para erros no Swagger
error_model = ns.model('Error', {
    'status': fields.String(description='Status (error)'),
    'message': fields.String(description='Descrição do erro')
})


# Função auxiliar para padronizar respostas de erro
def error_response(code, message):
    return {"status": "error", "message": message}, code


# ROTAS PRINCIPAIS

@ns.route('/allMessages')
class Mensagens(Resource):

    # -------------------- GET --------------------
    @ns.marshal_list_with(mensagem_model)
    @ns.response(200, "Lista retornada com sucesso")
    @ns.response(500, "Erro interno", error_model)
    def get(self):
        """Listar todas as mensagens"""
        try:
            mensagens = list(collection.find({}))

            # Converter _id para id
            for m in mensagens:
                m["id"] = str(m.pop("_id"))

            return mensagens

        except Exception as e:
            print("ERRO NO GET /allMessages:", e)

            import traceback
            traceback.print_exc()

            
            return error_response(500, f"Erro ao buscar mensagens: {str(e)}")

   
# -------------------- POST --------------------

    @ns.expect(mensagem_model)
    # @ns.marshal_with(mensagem_model)
    @ns.response(201, "Mensagem criada")
    @ns.response(400, "Dados inválidos", error_model)
    @ns.response(500, "Erro interno", error_model)
    def post(self):
        """Adicionar uma nova mensagem"""
        try:
            nova = api.payload

            # Validar campos obrigatórios
            if not nova.get("user") or not nova.get("msg") or not nova.get("to"):
                return error_response(
                    400,
                    "Campos obrigatórios faltando: user, msg, to"
                )

            # Pegar dados da mensagem
            nome = nova["user"]
            mensagem = nova["msg"]

            # Inserir mensagem do usuário no MongoDB
            resultado = collection.insert_one(nova)
            nova["id"] = str(resultado.inserted_id)

            # Remover _id caso exista
            nova.pop("_id", None)

            # Se a mensagem for para o atendente (bot)
            if nova["to"] == "atendente":
                print("ENTROU NO BOT")

                # Chamar o agente
                resposta = processar_mensagem(mensagem, nome)

                # Criar mensagem do bot
                msg_bot = {
                    "user": "atendente",
                    "msg": resposta,
                    "to": nome
                }

                # Salvar resposta do bot
                resultado_bot = collection.insert_one(msg_bot)
                msg_bot["id"] = str(resultado_bot.inserted_id)
                msg_bot.pop("_id", None)

                return {
                    "mensagem_usuario": nova,
                    "resposta_bot": msg_bot
                }, 201

            # Caso a mensagem não seja para o bot
            return nova, 201

        except Exception as e:
            return error_response(
                500,
                f"Erro ao criar mensagem: {str(e)}"
            )

            

#  ROTAS COM ID — PUT e DELETE

@ns.route('/<string:id>')
class Mensagem(Resource):

    # -------------------- PUT --------------------
    @ns.expect(mensagem_model)
    @ns.marshal_with(mensagem_model)
    @ns.response(200, "Mensagem atualizada")
    @ns.response(400, "ID inválido", error_model)
    @ns.response(404, "Mensagem não encontrada", error_model)
    @ns.response(500, "Erro interno", error_model)
    def put(self, id):
        """Editar uma mensagem"""
        if not ObjectId.is_valid(id):
            return error_response(400, "ID inválido.")

        dados = api.payload

        try:
            resultado = collection.update_one({"_id": ObjectId(id)}, {"$set": dados})

            if resultado.matched_count == 0:
                return error_response(404, "Mensagem não encontrada.")

            dados["id"] = id
            return dados

        except Exception as e:
            return error_response(500, f"Erro ao atualizar: {str(e)}")

    # -------------------- DELETE --------------------
    @ns.response(200, "Mensagem deletada com sucesso")
    @ns.response(400, "ID inválido", error_model)
    @ns.response(404, "Mensagem não encontrada", error_model)
    @ns.response(500, "Erro interno", error_model)
    def delete(self, id):
        """Deletar uma mensagem"""
        if not ObjectId.is_valid(id):
            return error_response(400, "ID inválido.")

        try:
            resultado = collection.delete_one({"_id": ObjectId(id)})

            if resultado.deleted_count == 0:
                return error_response(404, "Mensagem não encontrada.")

            return {"status": "success", "id": id}

        except Exception as e:
            return error_response(500, f"Erro ao deletar mensagem: {str(e)}")
        

# ROTAS PRINCIPAIS

#---------------------- GET DO USUÁRIO -----------------------------
        
@ns_users.route('/')
class Usuario(Resource):

        def get(self):
            usuarios = list(users_collection.find({}))

            for u in usuarios:
                u["id"] = str(u.pop("_id"))

            return usuarios 
        
# ------------------------------ POST DE USUÁRIO ---------------------------------        

        @ns.expect(usuario_model)
        def post(self):

            novo_usuario = api.payload

            if not novo_usuario.get("name") or not novo_usuario.get("email") or not novo_usuario.get("password"):
                return {
                    "status": "error",
                    "message": "Campos obrigatórios: name, email e password"
                }, 400
            
            resultado = users_collection.insert_one(novo_usuario)

            novo_usuario["id"] = str(resultado.inserted_id)

           

            return novo_usuario, 201
        

# ---------------------- PUT DO USUARIO -----------------------------      

@ns_users.route('/<string:id>')
class UsuarioId(Resource): 

        @ns.expect(usuario_model)
        def put(self, id):

            # Verifica se o ID é válido
            if not ObjectId.is_valid(id):
                return error_response(400, "ID inválido.")

            dados = api.payload

            try:
                resultado = users_collection.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": dados}
                )   

                if resultado.matched_count == 0:
                    return error_response(404, "Usuário não encontrado.")
                
                dados["id"] = id

                return dados
            except Exception as e:
                return error_response(500, f"Erro ao atualizar: {str(e)}")
            

        def delete(self, id):

             if not ObjectId.is_valid(id):
                return error_response(400, "ID inválido.")

             try:
                resultado = users_collection.delete_one(
                   {"_id": ObjectId(id)}
                )

                if resultado.deleted_count == 0:
                    return error_response(404, "Usuário não encontrado.")

                return {
                   "status": "success",
                    "message": "Usuário removido com sucesso",
                    "id": id
                }

             except Exception as e:
              return error_response(500, f"Erro ao deletar: {str(e)}")    
        

