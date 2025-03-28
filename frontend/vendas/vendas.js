document.addEventListener('DOMContentLoaded', function() {
  const produtoSelect = document.getElementById('produtoSelect');
  const addProdutoForm = document.getElementById('addProdutoForm');
  const produtosAdicionadosBody = document.getElementById('produtosAdicionadosBody');
  const totalVendaInfo = document.getElementById('totalVendaInfo');
  const finalizarVendaBtn = document.getElementById('finalizarVendaBtn');

  let produtosList = [];
  let carrinhoItens = [];

  // Fetch produtos list
  async function fetchProdutos() {
      try {
          const response = await fetch('http://127.0.0.1:5000/produtos');
          produtosList = await response.json();
          
          // Populate produto select
          produtoSelect.innerHTML = '<option value="">Selecione um Produto</option>';
          produtosList.forEach(produto => {
              const option = document.createElement('option');
              option.value = produto.id;
              option.textContent = `${produto.nome} - R$ ${produto.preco.toFixed(2)}`;
              produtoSelect.appendChild(option);
          });
      } catch (error) {
          console.error('Erro ao buscar produtos:', error);
      }
  }

  // Add product to cart
  addProdutoForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const produtoId = produtoSelect.value;
      const quantidade = parseInt(document.getElementById('quantidade').value);

      if (!produtoId || quantidade <= 0) {
          alert('Por favor, selecione um produto e insira uma quantidade válida.');
          return;
      }

      const produtoSelecionado = produtosList.find(p => p.id === parseInt(produtoId));

      if (!produtoSelecionado) {
          alert('Produto não encontrado.');
          return;
      }

      // Check stock availability
      if (quantidade > produtoSelecionado.quantidade_em_estoque) {
          alert(`Quantidade indisponível em estoque. Estoque atual: ${produtoSelecionado.quantidade_em_estoque}`);
          return;
      }

      const itemCarrinho = {
          ...produtoSelecionado,
          quantidade: quantidade,
          total: produtoSelecionado.preco * quantidade
      };

      // Check if product already in cart
      const existingItemIndex = carrinhoItens.findIndex(item => item.id === itemCarrinho.id);
      if (existingItemIndex > -1) {
          carrinhoItens[existingItemIndex].quantidade += quantidade;
          carrinhoItens[existingItemIndex].total = 
              carrinhoItens[existingItemIndex].preco * carrinhoItens[existingItemIndex].quantidade;
      } else {
          carrinhoItens.push(itemCarrinho);
      }

      atualizarListaProdutos();
      atualizarTotalVenda();

      // Reset form
      produtoSelect.value = '';
      document.getElementById('quantidade').value = '';
  });

  // Update product list
  function atualizarListaProdutos() {
      produtosAdicionadosBody.innerHTML = '';
      carrinhoItens.forEach((item, index) => {
          const row = document.createElement('tr');
          row.innerHTML = `
              <td>${item.nome}</td>
              <td>${item.quantidade}</td>
              <td>R$ ${item.preco.toFixed(2)}</td>
              <td>R$ ${item.total.toFixed(2)}</td>
              <td class="actions">
                  <button onclick="editarItem(${index})">Editar</button>
                  <button onclick="removerItem(${index})">Excluir</button>
              </td>
          `;
          produtosAdicionadosBody.appendChild(row);
      });
  }

  // Update total sale
  function atualizarTotalVenda() {
      const totalItens = carrinhoItens.reduce((total, item) => total + item.total, 0);
      totalVendaInfo.innerHTML = `
          <div><strong>Total dos Itens:</strong> R$ ${totalItens.toFixed(2)}</div>
          <div><strong>Desconto/Cupom:</strong> R$ 0,00</div>
          <div><strong>Total Final:</strong> R$ ${totalItens.toFixed(2)}</div>
      `;
  }

  // Edit item
  window.editarItem = function(index) {
      const novaQuantidade = prompt('Digite a nova quantidade:');
      if (novaQuantidade && !isNaN(novaQuantidade)) {
          const item = carrinhoItens[index];
          const quantidade = parseInt(novaQuantidade);

          if (quantidade > 0 && quantidade <= item.quantidade_em_estoque) {
              item.quantidade = quantidade;
              item.total = item.preco * quantidade;
              atualizarListaProdutos();
              atualizarTotalVenda();
          } else {
              alert('Quantidade inválida ou indisponível em estoque.');
          }
      }
  };

  // Remove item
  window.removerItem = function(index) {
      carrinhoItens.splice(index, 1);
      atualizarListaProdutos();
      atualizarTotalVenda();
  };

  // Finalize sale
  finalizarVendaBtn.addEventListener('click', async function() {
      if (carrinhoItens.length === 0) {
          alert('Adicione produtos antes de finalizar a venda.');
          return;
      }

      const formaPagamento = document.getElementById('formaPagamento').value;

      try {
          const response = await fetch('http://127.0.0.1:5000/realizaCompra', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  data: new Date().toISOString(),
                  total: carrinhoItens.reduce((total, item) => total + item.total, 0),
                  forma_pagamento: formaPagamento,
                  itens: carrinhoItens.map(item => ({
                      produto_id: item.id,
                      quantidade: item.quantidade,
                      preco_unitario: item.preco
                  }))
              })
          });

          if (response.ok) {
              alert('Venda realizada com sucesso!');
              // Reset cart and page state
              carrinhoItens = [];
              atualizarListaProdutos();
              atualizarTotalVenda();
          } else {
              const errorData = await response.json();
              alert(`Erro ao realizar venda: ${errorData.error}`);
          }
      } catch (error) {
          console.error('Erro ao finalizar venda:', error);
          alert('Erro ao finalizar venda. Tente novamente.');
      }
  });

  // Initial load
  fetchProdutos();
});