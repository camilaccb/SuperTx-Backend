from pydantic import BaseModel
from datetime import datetime

from model.abastecimento import Abastecimento

class AbastecimentoSchema(BaseModel):

    """ 
    Define como uma novo abastecimento a ser inserido deve ser representado
    
    """    
    tipo_combustivel: str
    valor_por_litro: float
    valor_total_abastecimento: float
    hora_abastecimento: datetime
    
def apresenta_abastecimento(abastecimento: Abastecimento):
    """ 
    Retorna uma representação de um abastecimento
    
    """
    return {  
        "tipo_combustivel": abastecimento.tipo_combustivel,
        "valor_por_litro": abastecimento.valor_por_litro,
        "valor_total_abastecimento": abastecimento.valor_total_abastecimento,
        "hora_abastecimento": abastecimento.hora_abastecimento
    }