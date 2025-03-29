                    ## 📌 softMarket - Sistema de Supermercado  📌

Este é um projeto de sistema de supermercado, com foco na gestão de produtos, fornecedores e clientes. O sistema permitirá o gerenciamento de estoque, pedidos de fornecedores e vendas realizadas no supermercado.

### 🔧 **Rotas da Aplicação**

- **GET /produtos**

 Obtém a lista de produtos cadastrados no sistema.
 
- **POST /produto**

  Cadastra um novo produto no sistema.

- **DELETE /produto/{id}**

 Exclui um produto do sistema, se não estiver em um pedido de estoque.

- **GET /fornecedores**

   Obtém a lista de fornecedores cadastrados no sistema.
  
- **POST /fornecedor**

  Cadastra um novo Fornecedor no sistema.

- **DELETE /fornecedor/{id}**

   Exclui um fornecedor do sistema, caso não esteja associado a produtos ou pedidos de estoque.

- **GET /pedidosEstoque**

  Descrição: Obtém a lista de pedidos de estoque.

- **POST /pedidoEstoque**

  Descrição: Realiza um pedido de estoque para reposição de produtos.

- **POST /realizaCompra**

  Descrição: Realiza a compra de um produto, alterando o estoque.

- **GET /relatorio...**

  Descrição: Realiza a construção de relatório para excel, por favor olhar a pasta de relatórios pois há varias opções, mas como exemplo: `/relatorio_forncedores_excel`
 

### 💾 **Banco de Dados**

  O banco de dados utilizado é o PostgreSQL. As tabelas principais do sistema incluem Produto, Fornecedor, Compra, itemCompra, Usuario e PedidoEstoque.

  [![](https://mermaid.ink/img/pako:eNqdVF2PmzAQ_CvIz7koEAIJr9c76VRVilT1pYqEtnhDXGEvZ2y11yT_veajCSG0pfUD4PF4dzxe9sgy4sgShvqdgFyD3CnPja0mbg15x3ZaD6GMJ7i3fX-FKqOFyj1FEq_gviAwXqkxo9vNrxaUERw4pihTrAy9WryldGAqhRJysH1PWmGGnHTqZDx3Ms7tq30-Xyj_I7wDM1V-vQdJGTA0knOLXHB6aoX_JW0Nla2z_TPcGzTl5PXgYNAIifUHpGUjZUTji0H5SLLUMEFg1hDH9P2j9F4hpFYJA1rQcLWyXwwZKEZETxJ8Y8AweC9y7yqdm9J5BTlIVKNX-qmytdZpNWQr1ApG6qiEqvpGmqcHqA7XVVRWepoKvCS-_eNOp4eH06lfyom3Y37i79g9kY6D-mu56jfcXh0MiL10U-J2Qf4Yls2YRGe14K69NFbumDmgc4rVLI57sIWpmWdHBSfz45vKWGK0xRnTZPMDS_ZQVG5my_qiuw51QUtQn4nkry1OsCH9oe1nTVtrKCw5su8siYJ5HPlx7C_jTbRZh_GMvTl0OQ9XYRSHcRTGm0UUn2fsRxNzMV_HwWoZBWGwWEerRRjOWK7rw3QCUXHUj2SVYYkfnH8CzxWahg?type=png)](https://mermaid.live/edit#pako:eNqdVF2PmzAQ_CvIz7koEAIJr9c76VRVilT1pYqEtnhDXGEvZ2y11yT_veajCSG0pfUD4PF4dzxe9sgy4sgShvqdgFyD3CnPja0mbg15x3ZaD6GMJ7i3fX-FKqOFyj1FEq_gviAwXqkxo9vNrxaUERw4pihTrAy9WryldGAqhRJysH1PWmGGnHTqZDx3Ms7tq30-Xyj_I7wDM1V-vQdJGTA0knOLXHB6aoX_JW0Nla2z_TPcGzTl5PXgYNAIifUHpGUjZUTji0H5SLLUMEFg1hDH9P2j9F4hpFYJA1rQcLWyXwwZKEZETxJ8Y8AweC9y7yqdm9J5BTlIVKNX-qmytdZpNWQr1ApG6qiEqvpGmqcHqA7XVVRWepoKvCS-_eNOp4eH06lfyom3Y37i79g9kY6D-mu56jfcXh0MiL10U-J2Qf4Yls2YRGe14K69NFbumDmgc4rVLI57sIWpmWdHBSfz45vKWGK0xRnTZPMDS_ZQVG5my_qiuw51QUtQn4nkry1OsCH9oe1nTVtrKCw5su8siYJ5HPlx7C_jTbRZh_GMvTl0OQ9XYRSHcRTGm0UUn2fsRxNzMV_HwWoZBWGwWEerRRjOWK7rw3QCUXHUj2SVYYkfnH8CzxWahg)



###  **Funcionalidades**

- Cadastro de produtos, fornecedores e Pedidos de estoque.
- Controle de estoque, com quantidade disponível e reposição por pedidos de estoque.
- Exclusão de produtos, fornecedores e pedidos, com verificações de dependências.

### Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [beeKeeper](https://www.beekeeperstudio.io/)
* [postgreSQL](https://www.postgresql.org/)

## Dependências e Versões Necessárias

* **Python** - Versão: 3.11.7
* **beeKeeper** - Versão: 5.1.4 
* **PostgreSQL** - Versão: 17.4
* **Postman for Windows** - Versão: 11.38.3


[![](https://mermaid.ink/img/pako:eNqFlN1u2jAUx1_F8jVlSYDlo9KkQgLtWloKtBczvbCwKZGSmDmO-oF4mGnXu9oj8GI1x-Ejg21RdJTj_8_Hfzu2l3gqGMcBfpZ0MUfj8HySIf1ckJDm87agkj2hs7MvqE06lNFcSYEYR10hMz7lTMinkgeoU4EGUrBCiQoRkiGnSfxOJRpwFjMAo1yJ7wWvgNEe7Ih0IWlF7Wo1oWr9W8biU0-uf8zi6XYgE9vA9cjeKSq9UbYlO8BcktLoMRACcEWOrKLS3I6MgPxKjNedvHXdBfn6lGvU4wcjmtgD_Ib0ovHxUl-C2AexusQm3oB-C_pYMJEj_e6r8Lyk-8DdVbmyYF6peAvkgESv06TI1z9Pb4E7oO6r1CmDAwCHh78G-qx_7ZbhHpDR7s_8qZt4DdSYhOIlSwRlmwH_ty_G0OfCJMPDZHSYmHgFTQ8kYrH6x4412KOZefx3zsSHw3Eetwmu4ZTLlMZMH8blRpxgNecpn-BAfzI-o0WiJniSrTRK9aKM3rIpDpQseA1LUTzPcTCjSa6zYsGo4mFM9aFOd60Lmn0TIt120R6VkH1z-uESAAQHS_yKA9uy61bLdR3LbdreZ9tv1vAbDtxWveH5vu_4jtNsWI3WqobfoahV9yzPcu2G2_T8hu15rZq-UzazKR3yjHHZEUWmcOA47uoD0HFgRA?type=png)](https://mermaid.live/edit#pako:eNqFlN1u2jAUx1_F8jVlSYDlo9KkQgLtWloKtBczvbCwKZGSmDmO-oF4mGnXu9oj8GI1x-Ejg21RdJTj_8_Hfzu2l3gqGMcBfpZ0MUfj8HySIf1ckJDm87agkj2hs7MvqE06lNFcSYEYR10hMz7lTMinkgeoU4EGUrBCiQoRkiGnSfxOJRpwFjMAo1yJ7wWvgNEe7Ih0IWlF7Wo1oWr9W8biU0-uf8zi6XYgE9vA9cjeKSq9UbYlO8BcktLoMRACcEWOrKLS3I6MgPxKjNedvHXdBfn6lGvU4wcjmtgD_Ib0ovHxUl-C2AexusQm3oB-C_pYMJEj_e6r8Lyk-8DdVbmyYF6peAvkgESv06TI1z9Pb4E7oO6r1CmDAwCHh78G-qx_7ZbhHpDR7s_8qZt4DdSYhOIlSwRlmwH_ty_G0OfCJMPDZHSYmHgFTQ8kYrH6x4412KOZefx3zsSHw3Eetwmu4ZTLlMZMH8blRpxgNecpn-BAfzI-o0WiJniSrTRK9aKM3rIpDpQseA1LUTzPcTCjSa6zYsGo4mFM9aFOd60Lmn0TIt120R6VkH1z-uESAAQHS_yKA9uy61bLdR3LbdreZ9tv1vAbDtxWveH5vu_4jtNsWI3WqobfoahV9yzPcu2G2_T8hu15rZq-UzazKR3yjHHZEUWmcOA47uoD0HFgRA)





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

  No Windows, baixe e instale pelo site oficial: https://www.postgresql.org/download/.
  
  No macOS, você pode usar o Homebrew:

   ```
  brew install postgresql
   ```

Se você estiver usando um banco de dados PostgreSQL, pode gerenciá-lo com ferramentas como:
 - Beekeeper (Utilizado neste projeto)
 - PGAdmin (que vem junto com o PostgreSQL)
 - DBeaver (uma ferramenta alternativa)
    
Abra qualquer uma dessas ferramentas (Beekeeper, PGAdmin, ou DBeaver) e crie um banco de dados chamado softmarket ou o nome de sua preferência. O Arquivo com as informações para criação estão inseridos no:

```
db.txt
```

Após a criação, certifique-se de que a configuração do banco esteja correta no arquivo de configuração do seu projeto, no `config.py` você PRECISA colocar as informações corretas
inseridas previamente na instalação do postgreSQL, o `usuário` e `senha` é substituído no seguinte código, e caso queira mudar o nome do banco, certifique-se de mudar aqui também (nome do banco de dados `softmarket`).

```
"postgresql://Usuario:Senha@localhost:5432/softmarket"
```

5. **Rodar a aplicação**

  Após instalar as dependências e configurar o banco de dados, execute o servidor Flask:

   ```
    flask run
   ```


  A aplicação deve começar a rodar. Você pode confirmar que está tudo funcionando corretamente verificando a seguinte mensagem no terminal:

  ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

## Utilizando o Postman Para API

Você pode baixar o postman ou utiliza-lo online para acessar as funcionalidades da api neste link:

- [postman.com](https://www.postman.com)

#### **POST/fornecedor**
- **Descrição:** Registra um novo Fornecedor.
  
- **Corpo da Requisição:**
- No Postman, selecione o método POST e insira a URL da rota:
 ```
 http://127.0.0.1:5000/fornecedor
 ```
    
- Vá até a aba "Body" e selecione a opção "raw" e escolha o formato JSON.
- Cole o seguinte corpo da requisição:
    
```
{
  "nome": "Fornecedor Y",
  "cnpj": "00.000.000/0001-00",
  "contato": "contato@fornecedor.com"
}

```
- Clique em **Send** para verificar a resposta. Com o sucesso você deve receber uma resposta com 201 Created:

```
"message": "Fornecedor cadastrado com sucesso!"
```

- O Método Get é necessário colocar o `fornecedor` no plural se quiser listar os fornecedores.

- o Método DELETE é necessário colocar o `id` do fornecedor cadastrado:

```
http://127.0.0.1:5000/fornecedor/<id>
```

#### **POST/produto**
 **Descrição:** Registra um novo produto.
  
- **Corpo da Requisição:**
  
- No Postman, selecione o método POST e insira a URL da rota:

  
 ```
 http://127.0.0.1:5000/produto
 ```
    
- Vá até a aba "Body" e selecione a opção "raw" e escolha o formato JSON.
- Cole o seguinte corpo da requisição:
    
```
  {
    "nome": "Arroz",
    "preco": 26.6,
    "quantidade_em_estoque": 100,
    "fornecedor_id": 1,
    "estoque_minimo":30
  }

```
- Clique em **Send** para verificar a resposta. Com o sucesso você deve receber uma resposta com 201 Created:
  

```
{
    "message": "Produto cadastrado com sucesso!"
}
```

- **IMPORTANTE: o Produto só pode ser cadastrado se um fornecedor estiver cadastrado devido as restrições de chave no Banco de Dados (Não existe produto sem fornecedor)**

- O Método Get é necessário colocar o `produto` no plural se quiser listar os produtos cadastrados.

- o Método DELETE é necessário colocar o `id` do produto cadastrado:

```
http://127.0.0.1:5000/produto/<id>
```


#### **GET/Relatorio**
**Descrição:** Gera um novo relatório. (olhar diferentes opções de relatório em `softMarket-Project\app\controllers\relatórios.py`)
  
- **Corpo da Requisição:**
- No Postman, selecione o método GET e insira a URL da rota:
  
 ```
 http://127.0.0.1:5000/relatorio_fornecedores_excel
 ```
    
- Não é necessário inserir nada no Body. 
- Clique na seta ao lado de send **Send and Download** para verificar a resposta. Com o sucesso você deve receber uma resposta com 201 Created:

```
  "message": "Cliente cadastrado com sucesso!"
```

- O Método Get é necessário colocar o `cliente` no plural.

- o Método DELETE é necessário colocar o `id` do fornecedor cadastrado:

```
http://127.0.0.1:5000/cliente/<id>
```

#### **POST/pedidoEstoque**
**Descrição:** Registra um novo pedido para Estoque.

  
- **Corpo da Requisição:**
- No Postman, selecione o método POST e insira a URL da rota:

 ```
 http://127.0.0.1:5000/pedidoEstoque
 ```
    
- Vá até a aba "Body" e selecione a opção "raw" e escolha o formato JSON.
- Cole o seguinte corpo da requisição:
    
```
{
  "produto_id": 1,
  "quantidade": 11,
  "fornecedor_id": 2
}
```

- Clique em **Send** para verificar a resposta. Com o sucesso você deve receber uma resposta com 201 Created:

```
  "message": "Pedido de estoque realizado com sucesso!"
```

- **IMPORTANTE: o Pedido para Estoque só pode ser cadastrado se um fornecedor e um produto que ele forneceu estiver cadastrado, devido as restrições de chave no Banco de Dados (Não existe produto sem fornecedor, e não existe pedido para estoque sem produto)**

#### **POST/realizaCompra**
**Descrição:** Registra uma nova compra.

  
- **Corpo da Requisição:**
- No Postman, selecione o método POST e insira a URL da rota:
  
 ```
 http://127.0.0.1:5000/realizaCompra
 ```
    
- Vá até a aba "Body" e selecione a opção "raw" e escolha o formato JSON.
- Cole o seguinte corpo da requisição:
    
```
    {
        "cliente_id": 1,
        "data":"2025-02-20",
        "total": 22.80
    }
```

- Clique em **Send** para verificar a resposta. Com o sucesso você deve receber uma resposta com 201 Created:

```
  "message": "Compra realizada com sucesso!"
```

- **IMPORTANTE: a compra só pode ser cadastrada se um cliente  estiver cadastrado, devido as restrições de chave no Banco de Dados (Não existe produto vendido sem comprador!)**

