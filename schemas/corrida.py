from pydantic import BaseModel
from datetime import datetime

from model.corrida import Corrida

class CorridaSchema(BaseModel):

    """ 
    Define como uma nova corrida deve ser inserida
    
    """    
    cliente: str
    tipo_corrida: str
    valor_corrida: float

class CorridaViewSchema(BaseModel):

    """ 
    Define como uma nova corrida a ser inserida deve ser representada
    
    """    
    cliente: str
    tipo_corrida: str
    valor_corrida: float
    hora_registro_corrida: datetime
    bandeira: str
    quilometragem: float
    gasto_combustivel: float
    valor_livre: float
    
def apresenta_corrida(corrida: Corrida):
    """ 
    Retorna uma representação da corrida
    
    """
    return {
        "cliente": corrida.cliente,
        "tipo_corrida": corrida.tipo_corrida,
        "valor_corrida": corrida.valor_corrida,
        "hora_registro_corrida": corrida.hora_registro_corrida,
        "bandeira": corrida.bandeira,
        "quilometragem": corrida.quilometragem,
        "gasto_combustivel": corrida.gasto_combustivel,
        "valor_livre": corrida.valor_livre
    }