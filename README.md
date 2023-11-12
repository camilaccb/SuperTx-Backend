# BuddyConnect
Projeto backend da sprint de **Desenvolvimento Full Stack Básico** do [curso de pós graduação de Engenharia de Sofware da PUC Rio](https://especializacao.ccec.puc-rio.br/especializacao/engenharia-de-software).

## Objetivo do projeto
Sistema web que possibilita encontrar mentores na área de tecnologia. Permite o cadastro de mentores, a visualização,atualização e deleção de dados dos mentores.

## Como executar
Para executar o projeto, siga os passos:
1. Clone o repositório
2. Crie um ambiente virtual utilizando o poetry. Caso precise de um passo a passo veja [aqui](https://github.com/camilaccb/BuddyConnect-Backend/blob/main/ambiente-virtual-poetry.md)
> É fortemente indicado o uso de ambientes virtuais do poetry, pois segue a orientação prevista na [PEP 621](https://peps.python.org/pep-0621/) 
3. Faça a instalação das dependências listadas no [arquivo pyproject.toml](https://github.com/camilaccb/BuddyConnect-Backend/blob/main/pyproject.toml):

```bash
poetry install
```

4. Execute a API

```bash
(env)$ flask run --host 0.0.0.0 --port 5000
```



