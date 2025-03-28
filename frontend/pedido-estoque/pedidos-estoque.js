document.addEventListener('DOMContentLoaded', function () {
    // Elementos do DOM
    const novoPedidoForm = document.getElementById('novoPedidoForm');
    const editarPedidoForm = document.getElementById('editarPedidoForm');
    const buscarPedidoForm = document.getElementById('buscarPedidoForm');
    const pedidosEstoqueCorpo = document.getElementById('pedidosEstoqueCorpo');
    const produtoSelect = document.getElementById('produtoSelect');
    const fornecedorSelect = document.getElementById('fornecedorSelect');
    const editProdutoSelect = document.getElementById('editProdutoSelect');
    const editFornecedorSelect = document.getElementById('editFornecedorSelect');
    const pedidoBuscar = document.getElementById('pedidoBuscar');
    const cancelarEdicaoBtn = document.getElementById('cancelarEdicao');
    const novoPedidoCard = document.getElementById('novoPedidoCard');
    const editarPedidoCard = document.getElementById('editarPedidoCard');

    novoPedidoCard.style.display = 'block'

    // Carregar produtos e fornecedores nos selects
    function carregarProdutos() {
        fetch('http://127.0.0.1:5000/produtos')
            .then(response => response.json())
            .then(produtos => {
                [produtoSelect, editProdutoSelect, pedidoBuscar].forEach(select => {
                    select.innerHTML = '<option value="">Selecione um Produto</option>';
                    produtos.forEach(produto => {
                        const option = document.createElement('option');
                        option.value = produto.id;
                        option.textContent = produto.nome;
                        select.appendChild(option);
                    });
                });
            })
            .catch(error => console.error('Erro ao carregar produtos:', error));
    }

    function carregarFornecedores() {
        fetch('http://127.0.0.1:5000/fornecedores')
            .then(response => response.json())
            .then(fornecedores => {
                [fornecedorSelect, editFornecedorSelect].forEach(select => {
                    select.innerHTML = '<option value="">Selecione um Fornecedor</option>';
                    fornecedores.forEach(fornecedor => {
                        const option = document.createElement('option');
                        option.value = fornecedor.id;
                        option.textContent = fornecedor.nome;
                        select.appendChild(option);
                    });
                });
            })
            .catch(error => console.error('Erro ao carregar fornecedores:', error));
    }

function listarPedidos(filtro = '') {
    fetch('http://127.0.0.1:5000/pedidosEstoque')
        .then(response => response.json())
        .then(data => {
            // Filtro mais robusto
            const pedidos = filtro 
                ? data.pedidos.filter(pedido => 
                    pedido.produto_nome.toLowerCase().includes(filtro.toLowerCase()) ||
                    pedido.fornecedor_nome.toLowerCase().includes(filtro.toLowerCase())
                )
                : data.pedidos;

            pedidosEstoqueCorpo.innerHTML = '';
            
            // Tratar caso de lista vazia
            if (pedidos.length === 0) {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td colspan="5" class="text-center">Nenhum pedido encontrado</td>`;
                pedidosEstoqueCorpo.appendChild(tr);
                return;
            }

            pedidos.forEach(pedido => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${pedido.produto_nome}</td>
                    <td>${pedido.quantidade}</td>
                    <td>${new Date(pedido.data_pedido).toLocaleDateString()}</td>
                    <td>${pedido.fornecedor_nome}</td>
                    <td>
                        <button class="btn btn-edit" data-id="${pedido.id}">Editar</button>
                        <button class="btn btn-delete" data-id="${pedido.id}">Excluir</button>
                    </td>
                `;
                pedidosEstoqueCorpo.appendChild(tr);
            });

            // Adicionar event listeners para editar e excluir
            document.querySelectorAll('.btn-edit').forEach(btn => {
                btn.addEventListener('click', editarPedido);
            });
            document.querySelectorAll('.btn-delete').forEach(btn => {
                btn.addEventListener('click', excluirPedido);
            });
        })
        .catch(error => console.error('Erro ao listar pedidos:', error));
}

    // Adicionar novo pedido
    novoPedidoForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const dadosPedido = {
            produto_id: produtoSelect.value,
            quantidade: document.getElementById('quantidadePedido').value,
            fornecedor_id: fornecedorSelect.value
        };

        fetch('http://127.0.0.1:5000/pedidoEstoque', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dadosPedido)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            listarPedidos();
            novoPedidoForm.reset();
        })
        .catch(error => {
            console.error('Erro ao adicionar pedido:', error);
            alert('Erro ao adicionar pedido');
        });
    });

    // Editar pedido
    function editarPedido(e) {
        const pedidoId = e.target.dataset.id;
        fetch(`http://127.0.0.1:5000/pedidosEstoque`)
            .then(response => response.json())
            .then(data => {
                const pedido = data.pedidos.find(p => p.id == pedidoId);
                if (pedido) {
                    document.getElementById('editPedidoId').value = pedido.id;
                    editProdutoSelect.value = pedido.produto_id;
                    document.getElementById('editQuantidadePedido').value = pedido.quantidade;
                    editFornecedorSelect.value = pedido.fornecedor_id;

                    novoPedidoCard.style.display = 'none';
                    editarPedidoCard.style.display = 'block';
                }
            })
            .catch(error => console.error('Erro ao buscar pedido:', error));
    }

    // Atualizar pedido
    editarPedidoForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const pedidoId = document.getElementById('editPedidoId').value;
        const dadosPedido = {
            produto_id: editProdutoSelect.value,
            quantidade: document.getElementById('editQuantidadePedido').value,
            fornecedor_id: editFornecedorSelect.value
        };

        fetch(`http://127.0.0.1:5000/pedidoEstoque/${pedidoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dadosPedido)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            listarPedidos();
            editarPedidoForm.reset();
            novoPedidoCard.style.display = 'block';
            editarPedidoCard.style.display = 'none';
        })
        .catch(error => {
            console.error('Erro ao atualizar pedido:', error);
            alert('Erro ao atualizar pedido');
        });
    });

    // Cancelar edição
    cancelarEdicaoBtn.addEventListener('click', function() {
        novoPedidoCard.style.display = 'block';
        editarPedidoCard.style.display = 'none';
        editarPedidoForm.reset();
    });

    // Excluir pedido
    function excluirPedido(e) {
        const pedidoId = e.target.dataset.id;
        if (confirm('Tem certeza que deseja excluir este pedido?')) {
            fetch(`http://127.0.0.1:5000/pedidoEstoque/${pedidoId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                listarPedidos();
            })
            .catch(error => {
                console.error('Erro ao excluir pedido:', error);
                alert('Erro ao excluir pedido');
            });
        }
    }

// Função para autocomplete de produtos na busca
function autocompleteProdutos(input) {
    input.addEventListener('input', function () {
        const filtro = input.value.toLowerCase();
        if (filtro.length < 2) return; // Evita buscas com poucos caracteres

        fetch('http://127.0.0.1:5000/produtos')
            .then(response => response.json())
            .then(produtos => {
                const sugestoes = produtos.filter(produto => produto.nome.toLowerCase().includes(filtro));
                mostrarSugestoes(input, sugestoes);
            })
            .catch(error => console.error('Erro ao buscar produtos:', error));
    });
}

// Exibir sugestões dinâmicas
function mostrarSugestoes(input, sugestoes) {
    let listaSugestoes = document.getElementById('listaSugestoes');
    if (!listaSugestoes) {
        listaSugestoes = document.createElement('ul');
        listaSugestoes.id = 'listaSugestoes';
        listaSugestoes.style.position = 'absolute';
        listaSugestoes.style.background = '#fff';
        listaSugestoes.style.border = '1px solid #ccc';
        input.parentNode.appendChild(listaSugestoes);
    }

    listaSugestoes.innerHTML = '';
    sugestoes.forEach(produto => {
        const item = document.createElement('li');
        item.textContent = produto.nome;
        item.onclick = () => {
            input.value = produto.nome;
            listaSugestoes.innerHTML = '';
        };
        listaSugestoes.appendChild(item);
    });
}

function listarPedidosAutocomplete(filtro = '') {
    fetch('http://127.0.0.1:5000/pedidosEstoque')
        .then(response => response.json())
        .then(data => {
            const pedidos = filtro
                ? data.pedidos.filter(pedido => pedido.produto_nome.toLowerCase().includes(filtro.toLowerCase()))
                : data.pedidos;

            pedidosEstoqueCorpo.innerHTML = '';
            if (pedidos.length === 0) {
                pedidosEstoqueCorpo.innerHTML = '<tr><td colspan="5" class="text-center">Nenhum pedido encontrado</td></tr>';
                return;
            }

            pedidos.forEach(pedido => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${pedido.produto_nome}</td>
                    <td>${pedido.quantidade}</td>
                    <td>${new Date(pedido.data_pedido).toLocaleDateString()}</td>
                    <td>${pedido.fornecedor_nome}</td>
                    <td>
                        <button class="btn btn-edit" data-id="${pedido.id}">Editar</button>
                        <button class="btn btn-delete" data-id="${pedido.id}">Excluir</button>
                    </td>
                `;
                pedidosEstoqueCorpo.appendChild(tr);
            });

            // Atribuir eventos aos botões após renderizar a tabela
            document.querySelectorAll('.btn-edit').forEach(button => {
                button.addEventListener('click', editarPedido);
            });

            document.querySelectorAll('.btn-delete').forEach(button => {
                button.addEventListener('click', excluirPedido);
            });
        })
        .catch(error => console.error('Erro ao listar pedidos:', error));
}




// Buscar pedido específico usando autocomplete
document.getElementById('buscarPedidoForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const filtroProduto = document.getElementById('pedidoBuscar').value.trim();

    if (filtroProduto) {
        listarPedidosAutocomplete(filtroProduto);
    } else {
        listarPedidosAutocomplete(); // Sem filtro
    }
});


    // Inicialização
    carregarProdutos();
    carregarFornecedores();
    listarPedidos();

    autocompleteProdutos(document.getElementById('pedidoBuscar'));
    listarPedidosAutocomplete();
});