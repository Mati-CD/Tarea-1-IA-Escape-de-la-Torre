import heapq
from typing import List, Tuple, Dict, Optional
from entorno import Entorno



def manhattan_heuristic(pos: Tuple[int, int], meta: Tuple[int, int]) -> float:
    """Distancia Manhattan (|f1 - f2| + |c1 - c2|), heurística admisible y consistente."""
    return float(abs(pos[0] - meta[0]) + abs(pos[1] - meta[1]))


def _reconstruir_camino(vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]], 
                        actual: Tuple[int, int]) -> List[Tuple[int, int]]:
    camino = [actual]
    while vino_de[actual] is not None:
        actual = vino_de[actual]
        camino.append(actual)
    camino.reverse()
    return camino


def greedy_best_first_search(entorno: Entorno, inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Greedy Best-First Search: f(n) = h(n)."""
    if inicio == meta:
        return [inicio]

    contador = 0
    frontera = []
    h_inicial = manhattan_heuristic(inicio, meta)
    heapq.heappush(frontera, (h_inicial, contador, inicio))

    vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    visitados = {inicio}

    while frontera:
        _, _, actual = heapq.heappop(frontera)

        if actual == meta:
            return _reconstruir_camino(vino_de, actual)

        for vecino in entorno.obtener_vecinos(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                vino_de[vecino] = actual
                h_vecino = manhattan_heuristic(vecino, meta)
                contador += 1
                heapq.heappush(frontera, (h_vecino, contador, vecino))

    return []


def a_star_search(entorno: Entorno, inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """A* Search: f(n) = g(n) + h(n)."""
    if inicio == meta:
        return [inicio]

    contador = 0
    h_inicial = manhattan_heuristic(inicio, meta)
    frontera = []
    heapq.heappush(frontera, (h_inicial, h_inicial, contador, inicio))

    vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    puntuacion_g: Dict[Tuple[int, int], float] = {inicio: 0.0}

    while frontera:
        f_actual, h_actual, _, actual = heapq.heappop(frontera)

        if actual == meta:
            return _reconstruir_camino(vino_de, actual)

        if puntuacion_g[actual] + h_actual > f_actual:
            continue

        for vecino in entorno.obtener_vecinos(actual):
            costo_paso = entorno.obtener_costo_paso(vecino)
            g_tentativa = puntuacion_g[actual] + costo_paso

            if vecino not in puntuacion_g or g_tentativa < puntuacion_g[vecino]:
                puntuacion_g[vecino] = g_tentativa
                h_vecino = manhattan_heuristic(vecino, meta)
                f_vecino = g_tentativa + h_vecino
                
                vino_de[vecino] = actual
                contador += 1
                heapq.heappush(frontera, (f_vecino, h_vecino, contador, vecino))

    return []