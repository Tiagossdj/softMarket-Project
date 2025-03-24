document.addEventListener('DOMContentLoaded', () => {
    const visualizarProdutoForm = document.getElementById('visualizarProdutoForm');
    const tabelaEstoque = document.querySelector('table tbody');

    // Função para carregar estoque
    async function carregarEstoque() {
        try {
            const response = await fetch('http://127.0.0.1:5000/produtos');
            if (!response.ok) {
                throw new Error('Erro ao carregar estoque');
            }
            const estoque = await response.json();
            atualizarTabelaEstoque(estoque);
        } catch (error) {
            console.error('Erro ao carregar estoque:', error);
            alert(error.message);
        }
    }

    // Visualizar Produto
    visualizarProdutoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const produtoNome = document.getElementById('produtoVisualizar').value.trim();

        try {
            // Buscar todos os produtos
            const response = await fetch('http://127.0.0.1:5000/produtos');
            if (!response.ok) {
                throw new Error('Erro ao buscar produtos');
            }
            const produtos = await response.json();

            // Filtrar produto pelo nome (case-insensitive)
            const produtoEncontrado = produtos.find(
                produto => produto.nome.toLowerCase().includes(produtoNome.toLowerCase())
            );

            if (!produtoEncontrado) {
                alert('Produto não encontrado');
                return;
            }

            // Destacar produto na tabela
            highlightProduto(produtoEncontrado.id);
        } catch (error) {
            console.error('Erro:', error);
            alert(error.message);
        }
    });

    // Função para destacar produto na tabela
    function highlightProduto(produtoId) {
        const linhas = tabelaEstoque.querySelectorAll('tr');
        linhas.forEach(linha => {
            linha.classList.remove('produto-destacado');
            if (linha.dataset.produtoId === produtoId.toString()) {
                linha.classList.add('produto-destacado');
                linha.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    tabelaEstoque.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const linha = e.target.closest('tr');
            const produtoId = linha.dataset.produtoId;
            const nomeProduto = linha.querySelector('td:first-child').textContent.trim();
    
            if (confirm(`Tem certeza que deseja excluir o produto ${nomeProduto} do estoque?`)) {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/produto/${produtoId}`, {
                        method: 'DELETE'
                    });
    
                    // Verifica se há conteúdo para ser parseado como JSON
                    const data = response.status !== 204 ? await response.json() : {};
    
                    if (!response.ok) {
                        throw new Error(data.message || 'Erro ao excluir produto');
                    }
    
                    // Remover a linha da tabela
                    linha.remove();
                    alert('Produto excluído com sucesso');
    
                    // Recarregar o estoque para garantir dados atualizados
                    await carregarEstoque();
                } catch (error) {
                    console.error('Erro:', error);
                    alert(error.message);
                }
            }
        }
    });


    // Função para atualizar a tabela de estoque
    function atualizarTabelaEstoque(estoque) {
        // Limpar tabela atual
        tabelaEstoque.innerHTML = '';

        // Adicionar novas linhas com dados atualizados
        estoque.forEach(produto => {
            const linha = document.createElement('tr');
            linha.dataset.produtoId = produto.id;
            if (produto.quantidade_em_estoque < produto.estoque_minimo) {
                linha.classList.add('low-stock');
            }
            linha.innerHTML = `
                <td>${produto.nome}</td>
                <td>${produto.quantidade_em_estoque}</td>
                <td class="${produto.quantidade_em_estoque < produto.estoque_minimo ? 'alert' : 'ok'}">
                    ${produto.quantidade_em_estoque < produto.estoque_minimo ? 'Abaixo do Estoque Mínimo' : 'Estoque OK'}
                </td>
                <td class="actions">
                    <button class="delete-btn">Excluir</button>
                </td>
            `;

            tabelaEstoque.appendChild(linha);
        });
    }

    // Carregar estoque inicial
    carregarEstoque();
});

// Estilos para destacar produto
const estiloDestaque = document.createElement('style');
estiloDestaque.textContent = `
    .produto-destacado {
        background-color: #e6f3ff !important;
        font-weight: bold;
    }
`;
document.head.appendChild(estiloDestaque);