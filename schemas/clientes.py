from pydantic import BaseModel, validator
from datetime import datetime
import re
from typing import List 

from model.clientes import Clientes

class ClienteSchema(BaseModel):

    """ 
    Define como uma novo cliente deve ser cadastrado
    
    """    
    
    cpf_cliente: str = "83738509020"
    nome: str = "Marilac"
    telefone: str = "85996662597"

    @validator('cpf_cliente')
    def verificar_cpf(cls,v):
        if re.search("[0-9]",v):
            return v
        else:
            raise ValueError("O cpf deve conter apenas números")
    
    @validator('telefone')
    def verificar_telefone(cls,v):
        padrao_telefone = r'(\d{2})9(\d{8})'  # DDD (2 digitos), 9, 8 digitos
        match = re.match(padrao_telefone,v)
        if match:
            ddd = match.group(1)
            if 10 <= int(ddd) <= 99:
                return v
        raise ValueError("Formato invalido para número de telefone ou DDD inválido")


class ClienteViewSchema(BaseModel):

    """ 
    Define como um novo cliente cadastrado deve ser representado
    
    """    
    cpf_cliente: str
    nome: str
    telefone: str
    data_cadastro: datetime

    
def apresenta_cliente(cliente: Clientes):
    """ 
    Retorna uma representação de um cliente cadastrado
    
    """
    return {
        "cpf_cliente": cliente.cpf_cliente,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "data_cadastro": cliente.data_cadastro
    }

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no cpf do cliente.
    """
    cpf: str = "83738509020"

    @validator('cpf')
    def verificar_cpf(cls,v):
        if not re.search("[0-9]",v):
            return v
        else:
            raise("O cpf deve conter apenas números")

class ClienteDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção
    """    
    cpf_cliente: str
    nome: str
    telefone: str
    data_cadastro: datetime


class ClienteValioso(BaseModel):
    """
    Define o esquema para representação de um cliente valioso
    """
    nome_cliente: str
    total_gasto: float

class ClienteRecorrenteSchema(BaseModel):
    """
    Defines como deve ser a estrutura de dado retornado após a requisição de recuperar os clientes mais valiosos
    """
    clientes_valiosos: List[ClienteValioso]