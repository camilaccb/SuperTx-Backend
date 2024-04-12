# Passo a passo para criar ambiente virtual usando Poetry

1. Instalar o poetry usando o pip
```bash
poetry install
```
2. Verificar se o poetry foi instalado
```bash
poetry --version
```
3. Configurar o poetry para que o ambiente virtual seja criado no diretório do projeto
```bash
poetry config virtualenvs.in-project true
```
4. Criar o o ambiente virtual no diretório do projeto
```bash
poetry init -n
```
