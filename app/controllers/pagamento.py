# Lista para armazenar os preços dos produtos
produtos = []

# Pergunta ao usuário quantos produtos ele comprou
num_produtos = int(input("Quantos produtos você comprou? "))

# Laço para capturar os preços de cada produto
for i in range(num_produtos):
    preco = float(input(f"Digite o preço do produto {i+1}: R$ "))
    produtos.append(preco)

# Calcula o subtotal
subtotal = sum(produtos)
print(f"Subtotal: R$ {subtotal:.2f}")

# Pergunta pela forma de pagamento
print("Escolha a forma de pagamento:")
print("1 - Cartão de Crédito")
print("2 - Cartão de Débito")
print("3 - Dinheiro")
print("4 - Pix")
opcao = int(input("Digite a opção escolhida (1-4): "))

# Verifica a forma de pagamento escolhida
if opcao == 1:
    pagamento = "Cartão de Crédito"
elif opcao == 2:
    pagamento = "Cartão de Débito"
elif opcao == 3:
    pagamento = "Dinheiro"
elif opcao == 4:
    pagamento = "Pix"
else:
    pagamento = "Opção inválida"

# Exibe o total e a forma de pagamento
print(f"Forma de pagamento escolhida: {pagamento}")
print(f"Total da compra: R$ {subtotal:.2f}")
