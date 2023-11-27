from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from  model import Base, Processo


class Cliente(Base):
    __tablename__ = 'cliente'

    cpf = Column(Float, primary_key=True)
    nome = Column(String(140), unique=True)
    telefone = Column(Integer)


    # Definição do relacionamento entre o cliente e o processo.
    # Essa relação é implicita, não está salva na tabela 'cliente',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    processos = relationship("Processo")

    def __init__(self, cpf:float, nome:str, telefone:int):
        """
        Cria um Cliente

        Arguments:
            cpf: cpf do cliente.
            nome: nome do Cliente.
            telefone: número de telefone do cliente
        """
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone


    def adiciona_processo(self, processo:Processo):
        """ Adiciona um novo processo ao cliente
        """
        self.processos.append(processo)
