import heapq
import time
from itertools import count
from typing import Callable, Dict, Optional, Set, Tuple

OBJETIVO = "12345678_"
POSICOES_OBJETIVO = {
    valor: (indice // 3, indice % 3) for indice, valor in enumerate(OBJETIVO)
}

class Nodo:
    def __init__(self, estado: str, pai: 'Nodo', acao: str, custo: int):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

def sucessor(estado: str) -> Set[Tuple[str, str]]:
    if len(estado) != 9 or "_" not in estado:
        raise ValueError("Estado inválido")

    index_branco = estado.index("_")
    linha, coluna = divmod(index_branco, 3)

    movimentos: Set[Tuple[str, str]] = set()

    def troca(pos_alvo: int, acao: str) -> None:
        lista_estado = list(estado)
        lista_estado[index_branco], lista_estado[pos_alvo] = (
            lista_estado[pos_alvo],
            lista_estado[index_branco],
        )
        movimentos.add((acao, "".join(lista_estado)))

    if coluna > 0:
        troca(index_branco - 1, "esquerda")
    if coluna < 2:
        troca(index_branco + 1, "direita")
    if linha > 0:
        troca(index_branco - 3, "acima")
    if linha < 2:
        troca(index_branco + 3, "abaixo")

    return movimentos

def expande(nodo: Nodo) -> Set[Nodo]:
    sucessores = sucessor(nodo.estado)
    filhos: Set[Nodo] = set()

    for acao, estado_sucessor in sucessores:
        filho = Nodo(
            estado=estado_sucessor,
            pai=nodo,
            acao=acao,
            custo=nodo.custo + 1,
        )
        filhos.add(filho)

    return filhos

def _heuristica_hamming(estado: str) -> int:
    return sum(
        1 for idx, valor in enumerate(estado)
        if valor != "_" and valor != OBJETIVO[idx]
    )

def _heuristica_manhattan(estado: str) -> int:
    distancia = 0
    for indice, valor in enumerate(estado):
        if valor == "_":
            continue
        linha_atual, coluna_atual = divmod(indice, 3)
        linha_obj, coluna_obj = POSICOES_OBJETIVO[valor]
        distancia += abs(linha_atual - linha_obj) + abs(coluna_atual - coluna_obj)
    return distancia

def _reconstroi_path(nodo: Nodo) -> list[str]:
    caminho: list[str] = []
    atual = nodo
    while atual.pai is not None:
        caminho.append(atual.acao)
        atual = atual.pai
    caminho.reverse()
    return caminho

def _tem_solucao(estado: str) -> bool:
    numeros = [char for char in estado if char != "_"]
    inversoes = 0
    for i in range(len(numeros)):
        for j in range(i + 1, len(numeros)):
            if numeros[i] > numeros[j]:
                inversoes += 1
    return inversoes % 2 == 0

def _a_star_com_metricas(
    estado_inicial: str,
    heuristica: Callable[[str], int],
) -> tuple[Optional[list[str]], int, float]:
    if len(estado_inicial) != 9 or "_" not in estado_inicial:
        raise ValueError("Estado invalido")

    if estado_inicial == OBJETIVO:
        return [], 0, 0.0

    if not _tem_solucao(estado_inicial):
        return None, 0, 0.0

    inicio = time.perf_counter()

    fronteira: list[Tuple[int, int, Nodo]] = []
    contador = count()

    nodo_inicial = Nodo(estado_inicial, None, None, 0)
    heapq.heappush(
        fronteira, (heuristica(estado_inicial), next(contador), nodo_inicial)
    )

    melhor_custo: Dict[str, int] = {estado_inicial: 0}
    explorados: Set[str] = set()
    nos_expandidos = 0

    while fronteira:
        _, _, atual = heapq.heappop(fronteira)

        if atual.estado in explorados:
            continue

        nos_expandidos += 1

        if atual.estado == OBJETIVO:
            fim = time.perf_counter()
            return _reconstroi_path(atual), nos_expandidos, fim - inicio

        explorados.add(atual.estado)

        for filho in expande(atual):
            g = filho.custo
            estado_filho = filho.estado

            if estado_filho in explorados and g >= melhor_custo.get(
                estado_filho, float("inf")
            ):
                continue

            if g < melhor_custo.get(estado_filho, float("inf")):
                melhor_custo[estado_filho] = g
                f = g + heuristica(estado_filho)
                heapq.heappush(fronteira, (f, next(contador), filho))

    fim = time.perf_counter()
    return None, nos_expandidos, fim - inicio

def astar_hamming_metricas(estado: str) -> tuple[Optional[list[str]], int, float]:
    return _a_star_com_metricas(estado, _heuristica_hamming)

def astar_manhattan_metricas(estado: str) -> tuple[Optional[list[str]], int, float]:
    return _a_star_com_metricas(estado, _heuristica_manhattan)

if __name__ == "__main__":
    estado = "2_3541687"

    ch, exp_h, tempo_h = astar_hamming_metricas(estado)
    cm, exp_m, tempo_m = astar_manhattan_metricas(estado)

    print("A* Hamming")
    print("  custo:", len(ch) if ch is not None else None)
    print("  nós expandidos:", exp_h)
    print("  tempo (s):", tempo_h)

    print("A* Manhattan")
    print("  custo:", len(cm) if cm is not None else None)
    print("  nós expandidos:", exp_m)
    print("  tempo (s):", tempo_m)