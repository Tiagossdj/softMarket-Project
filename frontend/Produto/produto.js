const precoInput = document.getElementById("productPrice");

precoInput.addEventListener("input", function () {
    // Remove tudo que não for número
    let valor = this.value.replace(/\D/g, "");

    // Se estiver vazio, exibe 0.00
    if (valor === "") {
        this.value = "0.00";
        return;
    }

    // Divide os centavos e formata
    let valorFormatado = (parseFloat(valor) / 100).toFixed(2);

    // Atualiza no input
    this.value = valorFormatado;
});




document.addEventListener("DOMContentLoaded", function () {
  const salvarProdutoBtn = document.getElementById("btnSalvarProduto");

  salvarProdutoBtn.addEventListener("click", async function (event) {
      event.preventDefault(); // evita recarregar a página

      const nome = document.getElementById("productName").value.trim();
      const preco = parseFloat(document.getElementById("productPrice").value.trim());
      const quantidade = parseInt(document.getElementById("productStock").value.trim());
      const estoqueMinimo = parseInt(document.getElementById("productMinStock").value.trim());
      const fornecedorId = parseInt(document.getElementById("productSupplier").value.trim());

      if (!nome || isNaN(preco) || isNaN(quantidade) || isNaN(estoqueMinimo) || isNaN(fornecedorId)) {
          alert("Preencha todos os campos corretamente.");
          return;
      }

      const produtoData = {
          nome: nome,
          preco: preco,
          quantidade_em_estoque: quantidade,
          estoque_minimo: estoqueMinimo,
          fornecedor_id: fornecedorId,
      };

      try {
          const response = await fetch("http://127.0.0.1:5000/produto", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(produtoData),
          });

          const result = await response.json();

          if (response.ok) {
              alert("Produto cadastrado com sucesso!");
              // Aqui você pode limpar os campos ou redirecionar
          } else {
              alert("Erro ao cadastrar produto: " + result.error);
          }
      } catch (error) {
          console.error("Erro:", error);
          alert("Erro ao cadastrar produto.");
      }
  });
});
