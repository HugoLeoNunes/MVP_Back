from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente

from schemas import ProcessoSchema


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido e como deve ser representado
    """
    cpf: float = 10010010050
    nome: str = "Joaquim José da Silva Nascimento"
    telefone: Optional[int] = 999991111


class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas pelo CPF do cliente.
    """
    cpf: float = 10010010050


class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "telefone": cliente.telefone,
        })

    return {"clientes": result}


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + processos.
    """
    cpf: float = 10010010050
    nome: str = "Joaquim José da Silva Nascimento"
    telefone: Optional[int] = 999991111
    processo: int = 10050017120238190001
    processos:List[ProcessoSchema]


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    cpf: float

def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    return {
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "total_processos": len(cliente.processos),
        "processos": [{"texto": c.texto} for c in cliente.processos]
    }
