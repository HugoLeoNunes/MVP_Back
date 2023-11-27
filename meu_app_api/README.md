# API de MVP

Esta é a primeira versão de um projeto (MVP) de uma aplicação Web, planejada para o controle de clientes e processos de um escritório de advocacia, voltado para pessoas com pouca afinidade com tecnologia.  


O objetivo aqui é demonstrar a usabilidade e a empregabilidade do aplicativo.

Ainda, destacar que todos os serviços ofertados pela aplicação, podem ter como suporte e, dependendo do contrato firmado, um escritório de advocacia com advogados de renome e grande arcabouço juridico, para auxiliar nas tramitações de seus processos. 

---

## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
