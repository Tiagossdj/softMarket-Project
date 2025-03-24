document.getElementById('fornecedorForm').addEventListener('submit', function(event) {
  event.preventDefault();  // Evita o envio padrão do formulário

  // Captura os dados do formulário
  const nome = document.getElementById('nome').value;
  const cnpj = document.getElementById('cnpj').value;
  const contato = document.getElementById('contato').value;

  // Cria o objeto com os dados
  const fornecedorData = {
      nome: nome,
      cnpj: cnpj,
      contato: contato
  };

  // Envia os dados para a rota de cadastro via POST
  fetch('http://127.0.0.1:5000/fornecedor', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(fornecedorData)
  })
  .then(response => response.json())
  .then(data => {
      alert(data.message);  // Exibe a mensagem de sucesso
      // Limpa o formulário
      document.getElementById('fornecedorForm').reset();
      // Atualiza a lista de fornecedores
      carregarFornecedores();
  })
  .catch(error => {
      console.error('Erro ao cadastrar fornecedor:', error);
      alert('Erro ao cadastrar fornecedor');
  });
});

// Função para carregar a lista de fornecedores
function carregarFornecedores() {
  fetch('http://127.0.0.1:5000/fornecedores')  // A rota de obtenção de todos os fornecedores
  .then(response => response.json())
  .then(data => {
      const tabelaBody = document.querySelector('table tbody');
      tabelaBody.innerHTML = '';  // Limpa a tabela

      data.forEach(fornecedor => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
              <td>${fornecedor.id}</td>
              <td>${fornecedor.nome}</td>
              <td>${fornecedor.cnpj}</td>
              <td>${fornecedor.contato}</td>
              <td class="actions">
                  <button class="delete-btn" data-id="${fornecedor.id}">Excluir</button>
              </td>
          `;
          tabelaBody.appendChild(tr);
      });

      // Adiciona os eventos de clique nos botões de excluir após a tabela ser atualizada
      document.querySelectorAll('.delete-btn').forEach(button => {
          button.addEventListener('click', function() {
              const id = this.getAttribute('data-id');
              excluirFornecedor(id);
          });
      });
  })
  .catch(error => {
      console.error('Erro ao carregar fornecedores:', error);
  });
}

// Função para excluir fornecedor
function excluirFornecedor(id) {
  fetch(`http://127.0.0.1:5000/fornecedor/${id}`, {
      method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
      alert(data.message);  // Exibe a mensagem de sucesso
      carregarFornecedores();  // Atualiza a lista de fornecedores após exclusão
  })
  .catch(error => {
      console.error('Erro ao excluir fornecedor:', error);
      alert('Erro ao excluir fornecedor');
  });
}

// Chama a função ao carregar a página para mostrar a lista inicial de fornecedores
document.addEventListener('DOMContentLoaded', carregarFornecedores);
