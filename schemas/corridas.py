from pydantic import BaseModel, validator
from datetime import datetime
import re

from model.corrida import Corridas

class CorridaSchema(BaseModel):

    """ 
    Define como uma nova corrida deve ser inserida
    
    """    
    
    id_cliente: str = "83738509020"
    tipo_corrida: str = "aplicativo"
    valor_corrida: float = "10.50"

    @validator('id_cliente')
    def verificar_cpf(cls,v):
        if re.search("[0-9]",v):
            return v
        else:
            raise ValueError("O cpf deve conter apenas números")

    @validator('tipo_corrida')
    def verificar_tipo_corrida(cls,v):
        if v not in ("aplicativo", "cliente", "rua"):
            raise ValueError(f"Tipo de corrida inválido")
        return v
            

class CorridaViewSchema(BaseModel):

    """ 
    Define como uma nova corrida a ser inserida deve ser representada
    
    """    
    id_cliente: str
    tipo_corrida: str
    valor_corrida: float
    hora_registro_corrida: datetime
    
def apresenta_corrida(corrida: Corridas):
    """ 
    Retorna uma representação da corrida
    
    """
    return {
        "id_cliente": corrida.id_cliente,
        "tipo_corrida": corrida.tipo_corrida,
        "valor_corrida": corrida.valor_corrida,
        "hora_registro_corrida": corrida.hora_registro_corrida
    }