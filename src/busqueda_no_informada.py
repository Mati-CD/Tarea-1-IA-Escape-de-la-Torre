from collections import deque
import heapq
from typing import List, Tuple, Dict, Optional
from entorno import Entorno


def _reconstruir_camino(vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]], 
                        actual: Tuple[int, int]) -> List[Tuple[int, int]]:
    camino = [actual]
    while vino_de[actual] is not None:
        actual = vino_de[actual]
        camino.append(actual)
    camino.reverse()
    return camino


def breadth_first_search(entorno: Entorno, inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Búsqueda en Anchura (BFS): minimiza la cantidad de transiciones unitarias."""
    if inicio == meta:
        return [inicio]

    frontera = deque([inicio])
    vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}

    while frontera:
        actual = frontera.popleft()

        for vecino in entorno.obtener_vecinos(actual):
            if vecino not in vino_de:
                vino_de[vecino] = actual
                if vecino == meta:
                    return _reconstruir_camino(vino_de, vecino)
                frontera.append(vecino)

    return []


def uniform_cost_search(entorno: Entorno, inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Búsqueda de Costo Uniforme (UCS): minimiza el costo acumulado considerando congestión."""
    if inicio == meta:
        return [inicio]

    contador = 0
    frontera = []
    heapq.heappush(frontera, (0.0, contador, inicio))

    vino_de: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    costo_acumulado: Dict[Tuple[int, int], float] = {inicio: 0.0}

    while frontera:
        costo_actual, _, actual = heapq.heappop(frontera)

        if actual == meta:
            return _reconstruir_camino(vino_de, actual)

        if costo_actual > costo_acumulado[actual]:
            continue

        for vecino in entorno.obtener_vecinos(actual):
            costo_paso = entorno.obtener_costo_paso(vecino)
            nuevo_costo = costo_actual + costo_paso

            if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                costo_acumulado[vecino] = nuevo_costo
                vino_de[vecino] = actual
                contador += 1
                heapq.heappush(frontera, (nuevo_costo, contador, vecino))

    return []