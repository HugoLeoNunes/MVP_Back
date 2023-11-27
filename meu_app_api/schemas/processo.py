from pydantic import BaseModel


class ProcessoSchema(BaseModel):
    """ Define como o número do processo a ser inserido e como deve ser representado
    """
    processo: int = 10050017120238190001
    cliente_cpf: float = 100-100-100-50
    texto: str = "Processo em fase de clnclusão. Aguardando despacho do MM. Juiz"
