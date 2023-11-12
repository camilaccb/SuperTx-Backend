"""
API da aplicação que utiliza a lib flask-openapi3 para gerar a documentação automaticamente a partir do código

"""

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect 
from flask_cors import CORS


# Inclui metadados da API
info = Info(title="BuddyConnect API", version="1.0.0")
app = OpenAPI(__name__, info = info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")


# Rotas da API (endpoints, paths, views)
@app.get('/', tags=[home_tag])
def home():
   
    return redirect('/openapi')

