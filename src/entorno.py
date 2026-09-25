from collections import defaultdict
from typing import List, Tuple, Set, Dict

# Constantes de representación de celdas
VACIO = 0
MURO = 1
SALIDA = 2
FUEGO = 3

# Acciones discretas de desplazamiento ortogonal y espera
ACCIONES = {
    'ARRIBA': (-1, 0),
    'ABAJO': (1, 0),
    'IZQUIERDA': (0, -1),
    'DERECHA': (0, 1),
    'ESPERAR': (0, 0)
}

class Entorno:
    def __init__(self, matriz_tablero: List[List[int]], pos_salida: Tuple[int, int], 
                 k_propagacion_fuego: int = 3, capacidad_maxima: int = 2, penalizacion_alfa: float = 1.5):
        """
        :param matriz_tablero: Matriz 2D con los muros, celdas vacías y la salida única.
        :param pos_salida: Coordenada (fila, columna) de la zona de escape.
        :param k_propagacion_fuego: Cada cuántos turnos se expanden las llamas.
        :param capacidad_maxima: Capacidad nominal de personas por celda.
        :param penalizacion_alfa: Factor de escala para la penalización cuadrática por congestión.
        """
        self.filas = len(matriz_tablero)
        self.columnas = len(matriz_tablero[0])
        self.tablero = [fila[:] for fila in matriz_tablero]
        self.pos_salida = pos_salida
        self.k_propagacion_fuego = k_propagacion_fuego
        self.capacidad_maxima = capacidad_maxima
        self.penalizacion_alfa = penalizacion_alfa
        
        self.celdas_fuego: Set[Tuple[int, int]] = set()
        self.ocupacion_celdas: Dict[Tuple[int, int], int] = defaultdict(int)
        self.turno_actual = 0

    def agregar_fuego_inicial(self, coordenadas_fuego: List[Tuple[int, int]]):
        """Ubica los focos de fuego iniciales en casillas no sólidas."""
        for f, c in coordenadas_fuego:
            if self.es_coordenada_valida(f, c) and self.tablero[f][c] != MURO:
                self.tablero[f][c] = FUEGO
                self.celdas_fuego.add((f, c))

    def es_coordenada_valida(self, f: int, c: int) -> bool:
        return 0 <= f < self.filas and 0 <= c < self.columnas

    def es_transitable(self, f: int, c: int) -> bool:
        """Verifica si la celda está dentro del mapa y no contiene muros ni fuego."""
        if not self.es_coordenada_valida(f, c):
            return False
        return self.tablero[f][c] not in (MURO, FUEGO)

    def obtener_vecinos(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Devuelve las celdas adyacentes transitables más la opción de permanecer en el lugar."""
        f, c = pos
        vecinos = []
        for _, (df, dc) in ACCIONES.items():
            nf, nc = f + df, c + dc
            if self.es_transitable(nf, nc):
                vecinos.append((nf, nc))
        return vecinos

    def obtener_costo_paso(self, pos_destino: Tuple[int, int]) -> float:
        """
        Calcula el costo de ingresar a una casilla en función de su nivel de congestión.
        Costo = 1 + penalizacion_alfa * (ocupantes)^2
        """
        ocupacion = self.ocupacion_celdas[pos_destino]
        return 1.0 + self.penalizacion_alfa * (ocupacion ** 2)

    def propagar_fuego(self):
        """Propaga las llamas de forma irreversible a las casillas libres vecinas."""
        nuevas_quemadas = set()
        for f, c in self.celdas_fuego:
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nf, nc = f + df, c + dc
                if self.es_coordenada_valida(nf, nc) and self.tablero[nf][nc] in (VACIO, SALIDA):
                    nuevas_quemadas.add((nf, nc))
        
        for f, c in nuevas_quemadas:
            self.tablero[f][c] = FUEGO
            self.celdas_fuego.add((f, c))

    def actualizar_ocupacion(self, agentes_activos: List['Agente']):
        """Actualiza el censo de personas por casilla tras cada ciclo de movimiento."""
        self.ocupacion_celdas.clear()
        for agente in agentes_activos:
            if agente.esta_vivo and not agente.ha_escapado:
                self.ocupacion_celdas[agente.pos] += 1