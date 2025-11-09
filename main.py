
from solucao import (
    Nodo,
    astar_hamming,
    astar_manhattan,
    expande,
    sucessor,
)

print(sucessor("2_3541687"))
# resposta: {('esquerda', '_23541687'), ('abaixo', '2435_1687'), ('direita', '23_541687')}

raiz = Nodo("2_3541687", None, None, 0)
filho = Nodo("_23541687", raiz, "esquerda", 1)

# Verificações
print(filho.pai is raiz)      # Deve ser True
print(filho.custo == raiz.custo + 1)  # Deve ser True

# Teste simples para expande
resultado_expande = expande(raiz)
esperado = {
    ("_23541687", "esquerda", 1),
    ("2435_1687", "abaixo", 1),
    ("23_541687", "direita", 1),
}

print(all(
    (nodo.estado, nodo.acao, nodo.custo) in esperado and nodo.pai is raiz
    for nodo in resultado_expande
))

print("4. Testes simples para A*")

# Testes simples para A*
print(astar_hamming("12345678_") == [])  # Estado já é solução
print(astar_manhattan("123456_78"))  # Deve retornar ['direita', 'direita']

resultado_hamming = astar_hamming("2_3541687")
resultado_manhattan = astar_manhattan("2_3541687")
print(len(resultado_hamming), len(resultado_manhattan))  # Ambos devem ter 23 ações

print(astar_hamming("185423_67"))  # Deve ser None
print(astar_manhattan("185423_67"))  # Deve ser None