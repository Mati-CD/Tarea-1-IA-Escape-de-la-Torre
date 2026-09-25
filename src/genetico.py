import random
from typing import List, Tuple
from entorno import Entorno, ACCIONES, MURO, FUEGO


GENES_DISPONIBLES = list(ACCIONES.keys())


class PlanificadorGenetico:
    def __init__(self, tam_poblacion: int = 40, longitud_cromosoma: int = 30, 
                 generaciones: int = 40, tasa_mutacion: float = 0.05, tasa_cruce: float = 0.8):
        self.tam_poblacion = tam_poblacion
        self.longitud_cromosoma = longitud_cromosoma
        self.generaciones = generaciones
        self.tasa_mutacion = tasa_mutacion
        self.tasa_cruce = tasa_cruce

    def _cromosoma_aleatorio(self) -> List[str]:
        return [random.choice(GENES_DISPONIBLES) for _ in range(self.longitud_cromosoma)]

    def _evaluar_adaptacion(self, cromosoma: List[str], entorno: Entorno, 
                            inicio: Tuple[int, int], meta: Tuple[int, int]) -> float:
        f_act, c_act = inicio
        costo_total = 0.0
        llego_a_meta = False
        pasos_usados = 0

        for indice, accion in enumerate(cromosoma):
            df, dc = ACCIONES[accion]
            nf, nc = f_act + df, c_act + dc

            if not entorno.es_coordenada_valida(nf, nc) or entorno.tablero[nf][nc] == MURO:
                costo_total += 80.0
                continue

            if entorno.tablero[nf][nc] == FUEGO:
                costo_total += 400.0
                f_act, c_act = nf, nc
                break

            f_act, c_act = nf, nc
            costo_total += entorno.obtener_costo_paso((f_act, c_act))

            if (f_act, c_act) == meta:
                llego_a_meta = True
                pasos_usados = indice + 1
                break

        distancia_restante = abs(f_act - meta[0]) + abs(c_act - meta[1])

        if llego_a_meta:
            aptitud = 2000.0 - (pasos_usados * 10.0) - costo_total
        else:
            aptitud = 1000.0 - (distancia_restante * 25.0) - costo_total

        return max(aptitud, 0.1)

    def _seleccion_torneo(self, poblacion: List[List[str]], aptitudes: List[float], k: int = 3) -> List[str]:
        indices_muestra = random.sample(range(len(poblacion)), k)
        mejor_indice = max(indices_muestra, key=lambda idx: aptitudes[idx])
        return poblacion[mejor_indice][:]

    def _cruce(self, padre1: List[str], padre2: List[str]) -> Tuple[List[str], List[str]]:
        if random.random() < self.tasa_cruce:
            punto = random.randint(1, self.longitud_cromosoma - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            return hijo1, hijo2
        return padre1[:], padre2[:]

    def _mutar(self, cromosoma: List[str]):
        for i in range(len(cromosoma)):
            if random.random() < self.tasa_mutacion:
                cromosoma[i] = random.choice(GENES_DISPONIBLES)

    def genetic_algorithm_search(self, entorno: Entorno, inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
        poblacion = [self._cromosoma_aleatorio() for _ in range(self.tam_poblacion)]
        mejor_cromosoma = poblacion[0]
        mejor_aptitud = -1.0

        for _ in range(self.generaciones):
            aptitudes = [self._evaluar_adaptacion(ind, entorno, inicio, meta) for ind in poblacion]

            for ind, apt in zip(poblacion, aptitudes):
                if apt > mejor_aptitud:
                    mejor_aptitud = apt
                    mejor_cromosoma = ind[:]

            nueva_poblacion = [mejor_cromosoma[:]]

            while len(nueva_poblacion) < self.tam_poblacion:
                p1 = self._seleccion_torneo(poblacion, aptitudes)
                p2 = self._seleccion_torneo(poblacion, aptitudes)
                h1, h2 = self._cruce(p1, p2)
                self._mutar(h1)
                self._mutar(h2)
                nueva_poblacion.append(h1)
                if len(nueva_poblacion) < self.tam_poblacion:
                    nueva_poblacion.append(h2)

            poblacion = nueva_poblacion

        return self._cromosoma_a_camino(mejor_cromosoma, entorno, inicio, meta)

    def _cromosoma_a_camino(self, cromosoma: List[str], entorno: Entorno, 
                            inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
        camino = [inicio]
        f_act, c_act = inicio

        for accion in cromosoma:
            df, dc = ACCIONES[accion]
            nf, nc = f_act + df, c_act + dc
            if entorno.es_coordenada_valida(nf, nc) and entorno.tablero[nf][nc] != MURO:
                f_act, c_act = nf, nc
            camino.append((f_act, c_act))
            if (f_act, c_act) == meta:
                break

        return camino