import heapq
from itertools import count
from typing import Callable, Dict, Optional, Set, Tuple

OBJETIVO = "12345678_"
POSICOES_OBJETIVO = {
    valor: (indice // 3, indice % 3) for indice, valor in enumerate(OBJETIVO)
}

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado: str, pai: 'Nodo', acao: str, custo: int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo


def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
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


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
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
        1 for idx, valor in enumerate(estado) if valor != "_" and valor != OBJETIVO[idx]
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


def _a_star(estado_inicial: str, heuristica: Callable[[str], int]) -> Optional[list[str]]:
    if len(estado_inicial) != 9 or "_" not in estado_inicial:
        raise ValueError("Estado invalido")

    if estado_inicial == OBJETIVO:
        return []

    if not _tem_solucao(estado_inicial):
        return None

    fronteira: list[Tuple[int, int, Nodo]] = []
    contador = count()

    nodo_inicial = Nodo(estado_inicial, None, None, 0)
    heapq.heappush(
        fronteira, (heuristica(estado_inicial), next(contador), nodo_inicial)
    )

    melhor_custo: Dict[str, int] = {estado_inicial: 0}
    explorados: Set[str] = set()

    while fronteira:
        _, _, atual = heapq.heappop(fronteira)

        if atual.estado in explorados:
            continue

        if atual.estado == OBJETIVO:
            return _reconstroi_path(atual)

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

    return None


def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    return _a_star(estado, _heuristica_hamming)


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    return _a_star(estado, _heuristica_manhattan)

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
