"""
API da aplicação que utiliza a lib flask-openapi3 para gerar a documentação automaticamente a partir do código

"""

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect,jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime, timedelta

from model import Session, Corridas, Clientes
from logger import logger
from schemas import *
from flask_cors import CORS

# Inclui metadados da API
info = Info(title="SuperTx API", version="1.0.0")
app = OpenAPI(__name__, info = info)

#Permite que outras origens realizem solicitações as rotas
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
corridas_tag = Tag(name="Corridas", description="Adição, visualização, atualização e deleção de uma corrida")
clientes_tag = Tag(name="Clientes", description="Adição, visualização, atualização e deleção de clientes")

# Rotas da API (endpoints, paths, views)
@app.get('/', tags=[home_tag])
def home():
   
    return redirect('/openapi')


@app.post('/corridas', tags=[corridas_tag],
          responses={"200": CorridaViewSchema , "409": ErrorSchema, "400": ErrorSchema})
def add_corrida(form: CorridaSchema):
    """
    Adiciona uma nova corrida na base

    Retorna uma representação da corrida inserida na base
    """
    
    id_cliente = form.id_cliente

    # Iniciando a sessão com o banco para adicionar a corrida
    session = Session()
    
    
    # Verifica se a corrida é de um cliente já cadastrado
    cliente = session.query(Clientes).filter_by(cpf_cliente = id_cliente).first() 

    # Retorna erro caso cliente não esteja cadastrado
    if not cliente:
        error_msg = "Cliente não cadastrado"
        logger.warning(error_msg)
        return {"mensagem": error_msg}, 409 
        
    
    corrida = Corridas(
    id_cliente = form.id_cliente,
    tipo_corrida = form.tipo_corrida,
    valor_corrida = form.valor_corrida
    )

    try:
        # adicionando corrida
        session.add(corrida)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado corrida")
        return apresenta_corrida(corrida), 200

    except IntegrityError as e:
        error_msg = "Corrida já salva na base"
        logger.warning(f"Corrida já adicionada")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar nova corrida :/"
        logger.warning(f"Erro ao adicionar corrida: {error_msg}")
        return {"mesage": error_msg}, 400

@app.post('/clientes', tags=[clientes_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """
    Adiciona uma novo cliente na base

    Retorna uma representação do cliente que foi cadastrado
    """

    cliente = Clientes(
    cpf_cliente = form.cpf_cliente,
    nome = form.nome,
    telefone = form.telefone
    )

    # Iniciando a sessão com o banco para adicionar o cliente
    session = Session()

    try:
        # adicionando cliente
        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela de cliente
        session.commit()
        logger.debug(f"Adicionado cliente")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        error_msg = "Cliente já salvo na base"
        logger.warning(f"Corrida já cadastrado")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível cadastrar o cliente :/"
        logger.warning(f"Erro ao cadastrar o cliente: {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.delete('/clientes', tags=[clientes_tag],
            responses={"200": ClienteDelSchema, "409": ErrorSchema, "400": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um cliente a partir do cpf informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cpf_cliente_deletar = query.cpf
    logger.debug(f"Deletando dados do cliente com cpf: {cpf_cliente_deletar}")
    
    # criando conexão com a base
    session = Session()
    
    # Verificando se o cliente possui corridas
    qtd_corridas = session.query(Corridas).filter(Corridas.id_cliente == cpf_cliente_deletar).count()

    # Retornar erro caso o cliente tenha corridas cadastradas
    if qtd_corridas:
        error_msg = "O cliente possui corridas associadas e não pode ser removido."
        logger.warning(f"Erro ao deletar cliente com cpf #{cpf_cliente_deletar}, {error_msg}")
        return {"message": error_msg}, 409
    
    # fazendo a remoção
    count = session.query(Clientes).filter(Clientes.cpf_cliente == cpf_cliente_deletar).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente com cpf #{cpf_cliente_deletar}")
        return {"mesage": "Cliente removido", "cpf": cpf_cliente_deletar}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente com cpf #'{cpf_cliente_deletar}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.get('/clientes', tags=[clientes_tag],
        responses={"200": ClienteRecorrenteSchema, "409": ErrorSchema, "400": ErrorSchema})
def recupera_clientes_recorrentes():
    """
    Retorna os clientes mais recorrentes e valiosos
    """
    # criando conexão com a base
    session = Session()

    ultimo_mes = datetime.now() - timedelta(days=30)

    #Executa query
    resultado_clientes_valiosos = session.query(Clientes.nome, func.sum(Corridas.valor_corrida).label('total_gasto')) \
                                    .join(Corridas) \
                                    .filter(Corridas.hora_registro_corrida >= ultimo_mes) \
                                    .group_by(Clientes.nome) \
                                    .order_by(func.sum(Corridas.valor_corrida).desc()) \
                                    .all()
    
    clientes_valiosos = []
    
    for cliente_valioso in resultado_clientes_valiosos:
        nome_cliente, total_gasto = cliente_valioso
        cliente_valioso_info = {
            "nome_cliente": nome_cliente,
            "total_gasto": total_gasto
        }
        clientes_valiosos.append(cliente_valioso_info)
    
    return jsonify(clientes_valiosos)