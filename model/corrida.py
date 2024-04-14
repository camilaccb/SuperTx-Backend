"""
Cria a classe relativa a entidade de corrida que vai ser utilizada no banco de dados

"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import Union


from model import Base

# Cria a classe Corridas a partir da classe Base (utiliza o conceito de herança)
class Corridas(Base):
    __tablename__ = "corridas"

    id_corrida = Column(Integer, primary_key=True)
    id_cliente = Column(String(11), ForeignKey("clientes.cpf_cliente"))
    tipo_corrida = Column(String)
    valor_corrida = Column(Float)
    hora_registro_corrida = Column(DateTime, default=datetime.now())

    clientes= relationship("Clientes",back_populates="corridas")


    def __init__(self, id_cliente: str,tipo_corrida: str, valor_corrida: float,hora_registo_corrida: Union[DateTime, None] = None):

        """
        Cria uma corrida

        Argumentos:
            cliente_id: id do cliente da corrida
            tipo_de_corrida: especifica se corrida foi na rua, por aplicativo ou contato direto do cliente
            valor_corrida: valor total em real da corrida
            hora_registro_corrida: dia e hora em que a corrida foi cadastrada no sistema
        """
        self.id_cliente = id_cliente
        self.tipo_corrida = tipo_corrida
        self.valor_corrida = valor_corrida
        self.hora_registro_corrida = hora_registo_corrida if hora_registo_corrida is not None else datetime.now()