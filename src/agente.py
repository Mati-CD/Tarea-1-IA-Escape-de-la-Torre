from typing import Tuple, List, Optional
from entorno import Entorno, FUEGO



class Agente:
    def __init__(self, id_agente: int, pos_inicial: Tuple[int, int]):
        self.id = id_agente
        self.pos = pos_inicial
        self.esta_vivo = True
        self.ha_escapado = False
        self.camino_planificado: List[Tuple[int, int]] = []
        self.turnos_activo = 0

    def decidir_siguiente_movimiento(self, entorno: Entorno, funcion_busqueda) -> Tuple[int, int]:
        """
        Determina la casilla objetivo inmediata. Replanifica si la ruta fue alcanzada por fuego.
        """
        necesita_replanificar = (
            not self.camino_planificado or 
            any(not entorno.es_transitable(f, c) for f, c in self.camino_planificado)
        )
        
        if necesita_replanificar:
            nuevo_camino = funcion_busqueda(entorno, self.pos, entorno.pos_salida)
            if nuevo_camino:
                # Se omite el primer elemento (casilla donde ya está parado el agente)
                self.camino_planificado = nuevo_camino[1:]
            else:
                self.camino_planificado = []

        if self.camino_planificado:
            return self.camino_planificado.pop(0)
        else:
            return self.pos  # Acción de esperar en caso de bloqueo

    def moverse_a(self, nueva_pos: Tuple[int, int], entorno: Entorno):
        """Ejecuta el desplazamiento y actualiza los indicadores de escape o baja."""
        self.pos = nueva_pos
        self.turnos_activo += 1

        if entorno.tablero[self.pos[0]][self.pos[1]] == FUEGO:
            self.esta_vivo = False
        elif self.pos == entorno.pos_salida:
            self.ha_escapado = True