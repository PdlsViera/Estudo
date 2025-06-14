from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de dados do usuário
class Usuario(BaseModel):
    nome: str
    idade: int
    email: str

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    return {
        "mensagem": "Usuário criado com sucesso!",
        "dados_recebidos": usuario
    }

@app.get("/")
def read_root():
    return {
        "Mensagem": "Olá, estou testando"
    }

# Modelo da lista
class Lista(BaseModel):
    nomeDaLista: str
    lista1: List[str]
    lista2: List[str]

@app.post("/lista")
def criar_lista(lista: Lista):
    listaTotal = lista.lista1 + lista.lista2
    return {
        "Lista": lista.nomeDaLista,
        "Itens recebidos": listaTotal,
        "Número de itens": len(listaTotal)
    }
