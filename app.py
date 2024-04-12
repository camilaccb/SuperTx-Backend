"""
API da aplicação que utiliza a lib flask-openapi3 para gerar a documentação automaticamente a partir do código

"""

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError


from model import Session, Corrida, Abastecimento
from logger import logger
from schemas import *
from flask_cors import CORS


# Inclui metadados da API
info = Info(title="BuddyConnect API", version="1.0.0")
app = OpenAPI(__name__, info = info)

#Permite que outras origens realizem solicitações as rotas
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
corridas_tag = Tag(name="Corridas", description="Adição, visualização, atualização e deleção de uma corrida")
abastecimento_tag = Tag(name="Abastecimento", description="Adição de abastecimento")


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
    corrida = Corrida(
        cliente = form.cliente,
        tipo_corrida = form.tipo_corrida,
        valor_corrida = form.valor_corrida
    )
    # Identifica a bandeira, calcula a quilometragem
    corrida.identificar_bandeira()
    corrida.calcular_quilometragem()

    # Iniciando a sessão com o banco para conseguir realizar consulta de último abastecimento
    session = Session()

    # Identifica último abastecimento e atualiza instância da corrida
    ultimo_abastecimento = session.query(Abastecimento).order_by(Abastecimento.id.desc()).first()
    if ultimo_abastecimento:
        logger.debug(f"Último abastecimento encontrado foi o do dia: '{ultimo_abastecimento.hora_abastecimento}'")
        corrida.calcular_gasto_combustivel(ultimo_abastecimento)
    else:
        # Último abastecimento não encontrado
        error_msg = "Último abastecimento não encontrado na base :/"
        logger.warning(f"Erro ao buscar último abastecimento, {error_msg}")
        return {"mesage": error_msg}, 404

    
    logger.debug(f"Adicionando corrida do cliente: {corrida.cliente}")
    try:
        # adicionando corrida
        session.add(corrida)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado corrida do cliente: {corrida.cliente}")
        return apresenta_corrida(corrida), 200

    except IntegrityError as e:
        # como a duplicidade da chave  cliente e datetime é a provável razão do IntegrityError
        error_msg = "Corrida já salva na base"
        logger.warning(f"Erro ao adicionar corrida do cliente '{corrida.cliente}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova corrida :/"
        logger.warning(f"Erro ao adicionar mentor '{corrida.cliente}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.post('/abastecimentos', tags=[abastecimento_tag],
          responses={"200": AbastecimentoSchema , "409": ErrorSchema, "400": ErrorSchema})
def add_abastecimento(form: AbastecimentoSchema):
    """
    Adiciona um novo abastecimento na base

    Retorna uma representação do abastecimento inserido na base
    """
    abastecimento = Abastecimento(
        tipo_combustível= form.tipo_combustivel,
        valor_por_litro = form.valor_por_litro,
        valor_total_abastecimento= form.valor_total_abastecimento
    )
    
    logger.debug(f"Adicionando o abastecimento do dia : {abastecimento.hora_abastecimento}")
    try:
        # Iniciando a sessão com o banco
        session = Session()
        # adicionando no abastecimento
        session.add(abastecimento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado o abastecimento do dia: {abastecimento.hora_abastecimento}")
        return apresenta_abastecimento(abastecimento), 200

    except IntegrityError as e:
        # como a duplicidade da chave  cliente e datetime é a provável razão do IntegrityError
        error_msg = "Abastecimento já salvo na base"
        logger.warning(f"Erro ao adicionar abastecimento do dia '{abastecimento.hora_abastecimento}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo abastecimento :/"
        logger.warning(f"Erro ao adicionar abastecimento do dia '{abastecimento.hora_abastecimento}', {error_msg}")
        return {"mesage": error_msg}, 400
    