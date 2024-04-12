"""
Cria a classe relativa a entidades que vão ser utilizadas no banco de dados

"""
from datetime import datetime, time
from sqlalchemy import Column, Integer, String, Float, DateTime
from typing import Union

from model import Base

# Cria a classe Abastecimento a partir da classe Base (utiliza o conceito de herança)
class Abastecimento(Base):
    __tablename__ = "abastecimentos"

    id = Column(Integer, primary_key=True)
    tipo_combustivel = Column(String)
    valor_por_litro = Column(Float)
    valor_total_abastecimento = Column(Float)
    hora_abastecimento = Column(DateTime, default=datetime.now())


    def __init__(self, tipo_combustível: str, valor_por_litro: float, valor_total_abastecimento: float, hora_abastecimento: Union[DateTime, None] = None):

        """
        Cria um abastecimento

        Argumentos:
            tipo_combustivel: especifica se o abastecimento foi com gasolina ou álcool
            valor_por_litro: valor em real do litro do combustível
            valor_total_abastecimento: valor total em real do abastecimento
            hora_registro_corrida: dia e hora em que o abastecimento foi feito
        """
        self.tipo_combustivel = tipo_combustível
        self.valor_por_litro = valor_por_litro
        self.valor_total_abastecimento = valor_total_abastecimento
        self.hora_abastecimento = hora_abastecimento if hora_abastecimento is not None else datetime.now()







        
