from sqlalchemy import Column, String, Integer, Float, ForeignKey
from  model import Base

class Processo(Base):
    __tablename__ = 'processo'

    processo = Column(Integer, primary_key=True)
    texto = Column(String(4000))

    # Definição do relacionamento entre o processo e um cliente.
    # Aqui está sendo definido a coluna 'cliente' que vai guardar
    # a referencia ao cpf do cliente, a chave estrangeira que relaciona
    # um cliente ao processo.

    cliente = Column(Float, ForeignKey("cliente.cpf"), nullable=False)

    def __init__(self, texto:str):
        
        """
        Cria um processo inerente a um cliente

        Arguments:
            texto: Breves comentários sobre o peocesso.
            Cabe, não olvidar, o relacionamento entre cliente e processo.
        """
        self.texto = texto
