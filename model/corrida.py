"""
Cria a classe relativa a entidade de corrida que vai ser utilizada no banco de dados

"""
from datetime import datetime, time
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from typing import Union


from model import Base
from model.abastecimento import Abastecimento

# Cria a classe Corrida a partir da classe Base (utiliza o conceito de herança)
class Corrida(Base):
    __tablename__ = "corridas"

    id = Column(Integer, primary_key=True)
    cliente = Column(String)
    tipo_corrida = Column(String)
    valor_corrida = Column(Float)
    hora_registro_corrida = Column(DateTime, default=datetime.now())
    bandeira = Column(String)
    quilometragem = Column(Float)
    gasto_combustivel = Column(Float)
    valor_livre = Column(Float)

    # Um cliente não pode ter mais de uma corrida registrada no mesmo dia e horário
    __table_args__ = (
       UniqueConstraint('cliente', 'hora_registro_corrida'),
    )

    def __init__(self, cliente: str, tipo_corrida: str, valor_corrida: float,hora_registro_corrida: Union[DateTime, None] = None):

        """
        Cria uma corrida

        Argumentos:
            cliente: nome do cliente da corrida
            tipo_de_corrida: especifica se corrida foi na rua, por aplicativo ou contato direto do cliente
            valor_corrida: valor total em real da corrida
            hora_registro_corrida: dia e hora em que a corrida foi cadastrada no sistema
        """
        self.cliente = cliente
        self.tipo_corrida = tipo_corrida
        self.valor_corrida = valor_corrida
        self.hora_registro_corrida = hora_registro_corrida if hora_registro_corrida is not None else datetime.now()
        
    def identificar_bandeira(self):
        """
        Identifica a bandeira a partir do dia e da hora da corrida
        """

        # Definir os limites para bandeira 1
        inicio_bandeira1_dia_util = time(6, 0)
        fim_bandeira1_dia_util = time(20, 0)
        fim_bandeira1_sabado = time(13, 0)

        # Obter apenas a parte do tempo (hora e minuto)
        hora_minuto = self.hora_registro_corrida.time()

        # Verificar se é dia útil ou sábado e está dentro do horário da bandeira 1
        if (self.hora_registro_corrida.weekday() < 5 and inicio_bandeira1_dia_util <= hora_minuto <= fim_bandeira1_dia_util) or \
        (self.hora_registro_corrida.weekday() == 5 and inicio_bandeira1_dia_util <= hora_minuto <= fim_bandeira1_sabado):
            self.bandeira= "1"
        else:
            self.bandeira= "2"

    def calcular_quilometragem(self):
        """
        Identifica a quantidade de quilometros rodados a partir 
        do valor da corrida e sabendo qual o valor do km de acordo
        com a bandeira
        """

        valor_por_km_b1 = 3.42
        valor_por_km_b2 = 4.49
        
        valor_bandeirada = 5.75
        valor_corrida_sem_bandeirada = self.valor_corrida - valor_bandeirada

        if self.bandeira == "1":
            valor_por_km = valor_por_km_b1
        else:
            valor_por_km = valor_por_km_b2

        self.quilometragem = valor_corrida_sem_bandeirada /valor_por_km

    def calcular_gasto_combustivel(self, abastecimento: Abastecimento):
        """
        Calcula o gasto de combustível e por decorrência o valor livre da corrida
        """
        consumo_carro_litro_por_km = 0.1

        self.gasto_combustivel = self.quilometragem * consumo_carro_litro_por_km * abastecimento.valor_por_litro
        self.valor_livre = self.valor_corrida - self.gasto_combustivel


        
