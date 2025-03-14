## 📌 softMarket - Sistema de Supermercado  📌

Este é um projeto de sistema de supermercado, com foco na gestão de produtos, fornecedores e clientes. O sistema permitirá o gerenciamento de estoque, pedidos de fornecedores, e vendas realizadas pelos clientes.

### 🔧 **Rotas da Aplicação**

- **POST /produto**  
  Cadastra um novo produto no sistema.
  
  Corpo da requisição:

```
{
  "nome": "Produto X",
  "preco": 10.50,
  "quantidade_em_estoque": 100,
  "fornecedor_id": 1
}

```

- **GET /produto**
  Obtém a lista de produtos cadastrados no sistema.

- **DELETE /produto/{id}**
  Exclui um produto do sistema, se não estiver em um pedido de estoque.

- **POST /fornecedor**  
  Cadastra um novo Fornecedor no sistema.
  
  Corpo da requisição:

```
{
  "nome": "Fornecedor Y",
  "cnpj": "00.000.000/0001-00",
  "contato": "contato@fornecedor.com"
}

```

- **GET /fornecedores**
  Obtém a lista de fornecedores cadastrados no sistema.

- **DELETE /fornecedor/{id}**
  Exclui um fornecedor do sistema, caso não esteja associado a produtos ou pedidos de estoque.

- **POST /cliente**  
  Cadastra um novo cliente no sistema.
  
  Corpo da requisição:

```
{
  "nome": "Cliente A",
  "cpf": "123.456.789-00",
  "email": "cliente@dominio.com"
}

```

- **GET /clientes**
  Obtém a lista de clientes cadastrados no sistema.

- **DELETE /cliente/{id}**
  Exclui um cliente do sistema.

- **POST /pedidoEstoque**
  Descrição: Realiza um pedido de estoque para reposição de produtos.

- **POST /realizaCompra**
  Descrição: Realiza a compra de um produto, alterando o estoque.
 

### 💾 **Banco de Dados**

  O banco de dados utilizado é o PostgreSQL. As tabelas principais do sistema incluem Produto, Fornecedor, Cliente, e PedidoEstoque.



### 🔐 **Funcionalidades**

- Cadastro de produtos, fornecedores e clientes.
- Controle de estoque, com quantidade disponível e reposição por pedidos de estoque.
- Exclusão de produtos, fornecedores e clientes, com verificações de dependências.

### Tecnologias Utilizadas

* [Python](Flask , SQLAlchemy(ORM)) (https://www.python.org/)
* [beeKeeper](https://www.beekeeperstudio.io/)
* [postgreSQL](https://www.postgresql.org/)

## Dependências e Versões Necessárias

* **Python** - Versão: 3.11.7
* **beeKeeper** - Versão: 5.1.4 
* **PostgreSQL** - Versão: 17.4 


[![](https://mermaid.ink/img/pako:eNptk-FOqzAUx1-l6efNwNh2lZvcRBmbU6dzQ01u8UNDqyMBOktJ1GVPcz_7FHuxWw-V2WFDGg7_H_2f9vRscCIYxz5-lnS9QtHod1wgPU7JtNh9JKl4RN3uH3RGAspoqaRAjKMgS3mh-KNBgQgsYixkwRPOhLSgkQXNpWCVEhYRkgWnWfpOJZpzljIAw1KJl8r2G-_BQORrSY1az2fATIjJFBlbyr7cAgDOyT7RNjMCZkpMnm0gBOCCtDJFJreGHAN5SepUG9lOegLQFZmE0cERn4MyA6V1tFMQr0G0j7Ser0C_AT0STJRIP2b90pAzYOY2s3dquGvgbm3OmJaW6w2QCxK-JllV7v79cHHmgCxtpLW9W6Aim_ppnwsA75qaww-7j6YGS9Dvv5f8EIkAeWgqfqjX8x1Qp3Vw_z14-ApwB-dc5jRlurU2n2KM1YrnPMa-fmX8iVaZinFcbDVKtdfyrUiwr2TFO1iK6nmF_SealTqq1owqPkqpbtG8-bqmxV8h9rG-gkrIWd3M0NPAYH-DX7Hf7TnD4ZE76Huup8fA9QYd_Ka_e87wyPkcXq_fd3snJ7-2HfwOC7tOrThOz-s7x95guP0PQdxGyw?type=png)](https://mermaid.live/edit#pako:eNptk-FOqzAUx1-l6efNwNh2lZvcRBmbU6dzQ01u8UNDqyMBOktJ1GVPcz_7FHuxWw-V2WFDGg7_H_2f9vRscCIYxz5-lnS9QtHod1wgPU7JtNh9JKl4RN3uH3RGAspoqaRAjKMgS3mh-KNBgQgsYixkwRPOhLSgkQXNpWCVEhYRkgWnWfpOJZpzljIAw1KJl8r2G-_BQORrSY1az2fATIjJFBlbyr7cAgDOyT7RNjMCZkpMnm0gBOCCtDJFJreGHAN5SepUG9lOegLQFZmE0cERn4MyA6V1tFMQr0G0j7Ser0C_AT0STJRIP2b90pAzYOY2s3dquGvgbm3OmJaW6w2QCxK-JllV7v79cHHmgCxtpLW9W6Aim_ppnwsA75qaww-7j6YGS9Dvv5f8EIkAeWgqfqjX8x1Qp3Vw_z14-ApwB-dc5jRlurU2n2KM1YrnPMa-fmX8iVaZinFcbDVKtdfyrUiwr2TFO1iK6nmF_SealTqq1owqPkqpbtG8-bqmxV8h9rG-gkrIWd3M0NPAYH-DX7Hf7TnD4ZE76Huup8fA9QYd_Ka_e87wyPkcXq_fd3snJ7-2HfwOC7tOrThOz-s7x95guP0PQdxGyw)



## Como rodar o projeto ✅

Para rodar a aplicação, siga os passos abaixo:

1. **Clonar o repositório**
   
    Primeiro, clone o repositório para sua máquina local:
   
 ```
  git clone git@github.com:Tiagossdj/softMarket-Project.git

 ```

Em seguida, entre no diretório do projeto:

 ```
  cd softMarket-project

 ```
  
 2. **Criar um Ambiente Virtual (opcional, mas recomendado)**

    Criar um ambiente virtual ajuda a gerenciar as dependências do seu projeto sem afetar o ambiente global do Python.

  Para criar o ambiente virtual:
  
  ```
  python3 -m venv venv

  ```

  Ative o ambiente virtual:

 - No Windows

  ```
  venv\Scripts\activate

  ```

- No macOS/Linux:

  ```
  source venv/bin/activate

  ```


3. **Instalar Dependências**

    Com o ambiente virtual ativo, instale as dependências necessárias:

  ```
  pip install -r requirements.txt

  ```

  Isso instalará o Flask, Flask-SQLAlchemy, psycopg2, entre outras dependências.

4. **Configurar o Banco de Dados**

  Se você ainda não tem um banco de dados PostgreSQL rodando, você pode configurá-lo da seguinte forma:
  - Instalar o PostgreSQL:

  No Windows, baixe e instale pelo site oficial: https://www.postgresql.org/download/
  No macOS, você pode usar o Homebrew:

   ```
  brew install postgresql

   ```
  - Configurar o Banco de Dados:

    Se você estiver usando um banco de dados PostgreSQL, pode gerenciá-lo com ferramentas como:
    - Beekeeper (Utilizado neste projeto)
    - PGAdmin (que vem junto com o PostgreSQL)
    - DBeaver (uma ferramenta alternativa)
    
    Abra qualquer uma dessas ferramentas (Beekeeper, PGAdmin, ou DBeaver) e crie um banco de dados chamado softmarket ou o nome de sua preferência.

    Após a criação, certifique-se de que a configuração do banco esteja correta no arquivo de configuração do seu projeto, como no config.py.

5. **Rodar a aplicação**

  Após instalar as dependências e configurar o banco de dados, execute o servidor Flask:

   ```
    python app.py

   ```


  A aplicação deve começar a rodar. Você pode confirmar que está tudo funcionando corretamente verificando a seguinte mensagem no terminal:

  ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


  ```
6. **Acessar a API**  

  Com a aplicação rodando, você pode usar o Postman ou qualquer outro cliente HTTP para testar as rotas da API.

  Exemplo de chamadas de API:
    - POST /produto: Cadastra um novo produto
    - GET /produto: Retorna todos os produtos cadastrados
    - POST /fornecedor: Cadastra um fornecedor
    - GET /fornecedor: Retorna todos os fornecedores cadastrados


