document.addEventListener('DOMContentLoaded', function () {
  const tabelaBody = document.querySelector('table tbody');
  const produtoVisualizarInput = document.getElementById('produtoVisualizar');
  const atualizarEstoqueBtn = document.querySelector('.update-stock button');
  
  const API_URL = 'http://127.0.0.1:5000/produtos';  // URL da API

  // Função para carregar todos os produtos
  function carregarProdutos(url) {
      fetch(url)  // Chamando a rota de produtos
          .then(response => response.json())  // Converte a resposta para JSON
          .then(data => {
              tabelaBody.innerHTML = '';  // Limpa a tabela antes de preencher

              // Verifique se há produtos na resposta
              if (data.length > 0) {
                  data.forEach(produto => {
                      const alerta = produto.quantidade_em_estoque < produto.estoque_minimo ? 'Abaixo do Estoque Mínimo' : 'Estoque OK';
                      const alertaClass = produto.quantidade_em_estoque < produto.estoque_minimo ? 'low-stock' : 'ok';

                      const tr = document.createElement('tr');  // Cria uma nova linha para o produto

                      // Adiciona a classe de alerta de estoque corretamente
                      if (alertaClass) {
                          tr.classList.add(alertaClass);  // Adiciona a classe para alerta de estoque
                      }

                      tr.innerHTML = `
                          <td>${produto.nome}</td>
                          <td>${produto.quantidade_em_estoque}</td>
                          <td class="${alertaClass === 'low-stock' ? 'alert' : 'ok'}">${alerta}</td>
                          <td class="actions">
                              <button class="delete-btn" data-id="${produto.id}">Excluir</button>
                          </td>
                      `;
                      tabelaBody.appendChild(tr);  // Adiciona a linha à tabela
                  });

                  // Adiciona evento de exclusão para cada botão "Excluir"
                  const deleteBtns = document.querySelectorAll('.delete-btn');
                  deleteBtns.forEach(btn => {
                      btn.addEventListener('click', function () {
                          const produtoId = btn.getAttribute('data-id');
                          excluirProduto(produtoId);
                      });
                  });
              } else {
                  tabelaBody.innerHTML = '<tr><td colspan="4">Nenhum produto encontrado.</td></tr>';  // Exibe uma mensagem caso não haja produtos
              }
          })
          .catch(error => {
              console.error('Erro ao carregar estoque:', error);
              tabelaBody.innerHTML = '<tr><td colspan="4">Erro ao carregar os produtos.</td></tr>';  // Exibe uma mensagem de erro
          });
  }

  // Função para excluir um produto
  function excluirProduto(id) {
      fetch(`http://127.0.0.1:5000/produto/${id}`, {
          method: 'DELETE',
      })
          .then(response => response.json())
          .then(data => {
              alert(data.message);  // Exibe a mensagem de sucesso ou erro
              carregarProdutos(API_URL);  // Atualiza a lista de produtos após exclusão
          })
          .catch(error => {
              console.error('Erro ao excluir produto:', error);
              alert('Erro ao excluir o produto.');
          });
  }

  // Função para filtrar produtos pelo nome
  produtoVisualizarInput.addEventListener('input', function () {
      const nomeProduto = produtoVisualizarInput.value.trim().toLowerCase();
      if (nomeProduto) {
          // Filtra os produtos com base no nome
          carregarProdutos(`${API_URL}?nome=${nomeProduto}`);
      } else {
          // Se o campo estiver vazio, carrega todos os produtos
          carregarProdutos(API_URL);
      }
  });

  // Evento para o botão de "Atualizar Estoque"
  atualizarEstoqueBtn.addEventListener('click', function () {
      carregarProdutos(API_URL);  // Simplesmente recarrega a lista de produtos
  });

  // Carrega todos os produtos inicialmente
  carregarProdutos(API_URL);
});
