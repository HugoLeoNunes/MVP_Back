from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cliente, Processo
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de clientes à base")
processo_tag = Tag(name="Processos", description="Adição de um processo e de um breve texto à um cliente cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação dos clientes e processos associados.
    """
    cliente = Cliente(
        cpf=form.cpf,
        nome=form.nome,
        telefone=form.telefone)
    logger.debug(f"Adicionando cliente de nome: '{cliente.cpf}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado o cpf do cliente: '{cliente.cpf}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo cpf já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.cpf}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.cpf}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os Clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes econtrados" % len(clientes))
        # retorna a representação de cliente
        print(clientes)
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um Cliente a partir do cpf do cliente

    Retorna uma representação dos clientes e processos associados.
    """
    cliente_cpf = query.cpf
    logger.debug(f"Coletando dados sobre clientes #{cliente_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first()

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{cliente.nome}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um Cliente a partir do cpf de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    
    cliente_cpf = query.cpf
    print(cliente_cpf)
    logger.debug(f"Deletando dados sobre o cliente selecionado #{cliente_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente #{cliente_cpf}")
        return {"mesage": "Cliente foi pro espaço", "id": cliente_cpf}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/processo', tags=[processo_tag],
          responses={"200": ClienteViewSchema, "404": ErrorSchema})
def add_processo(form: ProcessoSchema):
    """Adiciona de um novo prcoesso à um cliente cadastrado na base identificado pelo numero do processo, chamado somente por processo.

    Retorna uma representação dos clientes e processos associados.
    """
    cliente_cpf  = form.cliente_cpf
    logger.debug(f"Adicionando processos ao cliente #{cliente_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo cliente
    cliente = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first()

    if not cliente:
        # se cliente não encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao adicionar processo ao cliente '{cliente_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o Processo
    texto = form.texto
    num_processo = form.processo
    processo = Processo(num_processo,
                        texto)

    # relacionando o processo ao cliente
    cliente.adiciona_processo(processo)
    session.commit()

    logger.debug(f"Adicionado processo ao cliente #{cliente_cpf}")

    # retorna a representação do cliente
    return apresenta_cliente(cliente), 200
