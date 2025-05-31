# API de Administração da Academia de Cross Training (CrossX)

Este projeto implementa uma API RESTful para gerenciar informações de alunos, matrículas e pagamentos de uma academia de Cross Training.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

* Python (versão 3.8 ou superior recomendada)
* pip (gerenciador de pacotes do Python, geralmente vem com o Python)
* Git (para clonar o repositório)

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente:

1.  **Clone o Repositório:**
    Abra seu terminal ou prompt de comando e clone o repositório do GitHub:
    ```bash
    git clone https://github.com/WebersonCosta/crossx_api.git
    cd crossx_api # Ou o nome da pasta raiz do seu projeto
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

    * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * No macOS e Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    Após a ativação, seu prompt do terminal deve ser prefixado com `(venv)`.

3.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Executando a Aplicação

1.  **Inicie o Servidor Flask:**
    Após a instalação das dependências, você pode iniciar a API Flask:
    ```bash
    python run.py
    ```
    Por padrão, a API estará disponível em `http://127.0.0.1:5000/`.
    A base para os endpoints da API será `http://127.0.0.1:5000/api/v1/`.

2.  **Banco de Dados SQLite:**
    O projeto utiliza SQLite. O arquivo do banco de dados (`crossx.db`) será criado automaticamente dentro da pasta `instance/` na primeira vez que a aplicação for executada, e as tabelas também serão criadas.

## Testando a API

Recomendamos o uso de uma ferramenta cliente de API como [Thunder Client](https://www.thunderclient.com/) (extensão para VS Code), [Postman](https://www.postman.com/) ou [Insomnia](https://insomnia.rest/) para testar os endpoints.

**URL Base da API:** `http://127.0.0.1:5000/api/v1`

### Exemplos de Requisições para Iniciar:

1.  **Verificar Saúde da API (endpoint fora do prefixo `/api/v1`):**
    * **Método:** `GET`
    * **URL:** `http://127.0.0.1:5000/health`
    * **Resposta Esperada:** Status `200 OK`, Corpo: `"API Saudável!"`

2.  **Criar um Novo Aluno:**
    * **Método:** `POST`
    * **URL:** `http://127.0.0.1:5000/api/v1/alunos`
    * **Corpo (Body -> JSON):**
        ```json
        {
            "Nome": "Fulano de Tal",
            "Endereco": "Rua Teste, 123",
            "Cidade": "Sua Cidade",
            "Estado": "XX",
            "Telefone": "00912345678"
        }
        ```
    * **Resposta Esperada:** Status `201 Created`, com os dados do aluno criado e seu `ID_Aluno`.

3.  **Listar Todos os Alunos:**
    * **Método:** `GET`
    * **URL:** `http://127.0.0.1:5000/api/v1/alunos`
    * **Resposta Esperada:** Status `200 OK`, com uma lista dos alunos cadastrados.

### Endpoints Principais (Consulte o código ou documentação adicional para mais detalhes):

* **Alunos:**
    * `GET /alunos`: Lista todos os alunos.
    * `POST /alunos`: Cria um novo aluno.
    * `GET /alunos/<id>`: Obtém um aluno específico.
    * `PUT /alunos/<id>`: Atualiza um aluno.
    * `DELETE /alunos/<id>`: Exclui um aluno (sob condições específicas).
    * `POST /alunos/<id>/matricular`: Matricula um aluno.
    * `POST /alunos/<id>/desligar`: Desliga um aluno.
* **Pagamentos:**
    * `GET /alunos/<id>/pagamentos`: Lista pagamentos de um aluno.
    * `POST /alunos/<id>/pagamentos`: Registra um novo pagamento para um aluno.
    * `GET /pagamentos`: Lista todos os pagamentos (geral).
    * `GET /pagamentos/<id_pagamento>`: Obtém um pagamento específico.
    * `PUT /pagamentos/<id_pagamento>`: Atualiza um pagamento (opcional).
    * `DELETE /pagamentos/<id_pagamento>`: Exclui um pagamento (opcional).

## Estrutura do Projeto

```
crossx_api/
├── app/                # Contém a lógica principal da aplicação
│   ├── init.py     # Inicialização do Flask app e extensões
│   ├── models.py       # Modelos SQLAlchemy
│   ├── schemas.py      # Schemas Marshmallow
│   ├── resources.py    # Recursos da API (endpoints Flask-RESTful)
│   ├── config.py       # Configurações
│   └── ...
├── instance/           # Contém o arquivo do banco de dados SQLite (crossx.db)
├── venv/               # Ambiente virtual Python
├── requirements.txt    # Dependências do projeto
└── run.py              # Script para iniciar o servidor
```
