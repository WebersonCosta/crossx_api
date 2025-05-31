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

(Lembre-se de substituir `<id_aluno>` e `<id_pagamento>` pelos IDs reais obtidos durante os testes.)

---

### Endpoint de Verificação de Saúde

1.  **Verificar Saúde da API:**
    * **Ação:** Checa se a API está respondendo.
    * **Método:** `GET`
    * **URL:** `http://127.0.0.1:5000/health`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK`, Corpo: `"API Saudável!"`

---

### Endpoints de Alunos (`/alunos`)

1.  **Criar Novo Aluno:**
    * **Ação:** Adiciona um novo aluno.
    * **Método:** `POST`
    * **URL:** `/alunos`
    * **Corpo (Body -> JSON):**
        ```json
        {
            "Nome": "Carlos Silva",
            "Endereco": "Rua das Flores, 123",
            "Cidade": "Fortaleza",
            "Estado": "CE",
            "Telefone": "85999998888"
        }
        ```
    * **Resposta Esperada:** Status `201 Created` com os dados do aluno criado (anote o `ID_Aluno`).

2.  **Listar Todos os Alunos:**
    * **Ação:** Retorna uma lista de todos os alunos.
    * **Método:** `GET`
    * **URL:** `/alunos`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com a lista de alunos.

3.  **Consultar Aluno Específico:**
    * **Ação:** Retorna os detalhes de um aluno específico.
    * **Método:** `GET`
    * **URL:** `/alunos/<id_aluno>`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com os dados do aluno.

4.  **Atualizar Aluno:**
    * **Ação:** Modifica os dados de um aluno existente.
    * **Método:** `PUT`
    * **URL:** `/alunos/<id_aluno>`
    * **Corpo (Body -> JSON):**
        ```json
        {
            "Telefone": "85988887777",
            "Endereco": "Avenida Beira Rio, 456",
            "Data_Matricula": "2025-07-01"
        }
        ```
    * **Resposta Esperada:** Status `200 OK` com os dados do aluno atualizados. (Se `Data_Matricula` for alterada, `Data_Vencimento` e `Data_Desligamento` serão ajustadas pela API).

5.  **Matricular Aluno:**
    * **Ação:** Define ou atualiza a data de matrícula e vencimento de um aluno.
    * **Método:** `POST`
    * **URL:** `/alunos/<id_aluno>/matricular`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com mensagem de sucesso e a nova `data_vencimento`. Verifique o aluno com um `GET` para confirmar as datas.

6.  **Desligar Aluno:**
    * **Ação:** Registra a data de desligamento de um aluno.
    * **Método:** `POST`
    * **URL:** `/alunos/<id_aluno>/desligar`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com mensagem de sucesso e a `data_desligamento`. Verifique o aluno com um `GET` para confirmar.

7.  **Excluir Aluno:**
    * **Ação:** Remove o registro de um aluno. (Lembre-se das regras: só pode excluir se `Data_Desligamento` estiver preenchida e o aluno não estiver ativo).
    * **Método:** `DELETE`
    * **URL:** `/alunos/<id_aluno>`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` se a exclusão for permitida e bem-sucedida, ou `400 Bad Request` se as condições não forem atendidas.

---

### Endpoints de Pagamentos (`/pagamentos` e `/alunos/<id_aluno>/pagamentos`)

1.  **Registrar Novo Pagamento para um Aluno:**
    * **Ação:** Adiciona um registro de pagamento para um aluno específico.
    * **Método:** `POST`
    * **URL:** `/alunos/<id_aluno>/pagamentos`
    * **Corpo (Body -> JSON):**
        ```json
        {
            "Valor": 100.00,
            "Data": "2025-07-15", 
            "Tipo": "cartão"     
        }
        ```
    * **Resposta Esperada:** Status `201 Created` com os dados do pagamento (anote o `ID_Pagamento`). Verifique o aluno (`GET /alunos/<id_aluno>`) para ver o impacto na `Data_Vencimento`.

2.  **Listar Pagamentos de um Aluno Específico:**
    * **Ação:** Retorna todos os pagamentos feitos por um determinado aluno.
    * **Método:** `GET`
    * **URL:** `/alunos/<id_aluno>/pagamentos`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com a lista de pagamentos do aluno.

3.  **Listar Todos os Pagamentos (Geral):**
    * **Ação:** Retorna uma lista de todos os pagamentos registrados no sistema.
    * **Método:** `GET`
    * **URL:** `/pagamentos`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com a lista de todos os pagamentos.

4.  **Consultar Pagamento Específico:**
    * **Ação:** Retorna os detalhes de um pagamento específico.
    * **Método:** `GET`
    * **URL:** `/pagamentos/<id_pagamento>`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` com os dados do pagamento.

5.  **Atualizar Pagamento (Opcional):**
    * **Ação:** Modifica os dados de um pagamento existente.
    * **Método:** `PUT`
    * **URL:** `/pagamentos/<id_pagamento>`
    * **Corpo (Body -> JSON):**
        ```json
        {
            "Valor": 105.00,
            "Tipo": "dinheiro"
        }
        ```
    * **Resposta Esperada:** Status `200 OK` com os dados do pagamento atualizados.

6.  **Excluir Pagamento (Opcional):**
    * **Ação:** Remove o registro de um pagamento.
    * **Método:** `DELETE`
    * **URL:** `/pagamentos/<id_pagamento>`
    * **Corpo:** Nenhum.
    * **Resposta Esperada:** Status `200 OK` se a exclusão for bem-sucedida.

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
