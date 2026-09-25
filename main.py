import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from entorno import Entorno
from agente import Agente
from busqueda_no_informada import breadth_first_search, uniform_cost_search
from busqueda_informada import greedy_best_first_search, a_star_search
from genetico import PlanificadorGenetico
from simulacion import ejecutar_simulacion
from mapas import obtener_mapa_1


def ejecutar_demostracion():
    info_mapa = obtener_mapa_1()
    planificador_ga = PlanificadorGenetico(tam_poblacion=35, longitud_cromosoma=25, generaciones=35)

    algoritmos = {
        "1. Breadth-First Search": breadth_first_search,
        "2. Uniform Cost Search": uniform_cost_search,
        "3. Greedy Best-First Search": greedy_best_first_search,
        "4. A* Search": a_star_search,
        "5. Genetic Algorithm": planificador_ga.genetic_algorithm_search
    }

    print("=== TAREA 1: ESCAPE DE LA TORRE ===")
    print("Ejecución de prueba sobre el mapa de demostración:\n")

    for nombre, funcion_busqueda in algoritmos.items():
        entorno = Entorno(
            matriz_tablero=info_mapa["tablero"], 
            pos_salida=info_mapa["salida"], 
            k_propagacion_fuego=3
        )
        entorno.agregar_fuego_inicial(info_mapa["fuegos_iniciales"])

        agentes = [
            Agente(id_agente=1, pos_inicial=(2, 0)),
            Agente(id_agente=2, pos_inicial=(2, 2)),
            Agente(id_agente=3, pos_inicial=(4, 0)),
            Agente(id_agente=4, pos_inicial=(4, 3)),
        ]

        resultado = ejecutar_simulacion(entorno, agentes, funcion_busqueda, turnos_maximos=80)

        print(f"[{nombre}]")
        print(f" - Sobrevivientes : {resultado['sobrevivientes']} / {resultado['total_agentes']} ({resultado['tasa_supervivencia'] * 100:.1f}%)")
        print(f" - Tiempo despeje : {resultado['tiempo_despeje'] if resultado['tiempo_despeje'] is not None else 'Sin evacuados'} turnos")
        print(f" - Turnos totales : {resultado['turnos_totales']}\n")


if __name__ == "__main__":
    ejecutar_demostracion()