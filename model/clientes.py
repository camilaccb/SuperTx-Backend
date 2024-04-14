"""
Cria a classe relativa a entidade de clientes que vai ser utilizada no banco de dados

"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from typing import Union


from model import Base

# Cria a classe Clientes a partir da classe Base (utiliza o conceito de herança)
class Clientes(Base):
    __tablename__ = "clientes"

    cpf_cliente = Column(String(11), primary_key=True)
    nome = Column(String)
    telefone = Column(String(11), unique=True)
    data_cadastro = Column(DateTime, default=datetime.now())
    corridas = relationship("Corridas",back_populates="clientes")

    def __init__(self,cpf_cliente:str,nome: str, telefone: str, data_cadastro: Union[DateTime, None] = None):

        """
        Cria um cliente

        Argumentos:
            id: id do cliente cadastrado
            nome: nome do cliente cadastrado
            telefone: telefone com ddd do cliente cadastrado
            data_cadastro: dia e hora em que a corrida foi cadastrada no sistema, corresponde ao dia da primeira corrida
        """
        self.cpf_cliente = cpf_cliente
        self.nome = nome
        self.telefone = telefone
        self.data_cadastro = data_cadastro if data_cadastro is not None else datetime.now()
        

        
