import sys
import os
import random
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Callable

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from entorno import Entorno
from agente import Agente
from simulacion import ejecutar_simulacion
from busqueda_no_informada import breadth_first_search, uniform_cost_search
from busqueda_informada import greedy_best_first_search, a_star_search
from genetico import PlanificadorGenetico
from mapas import obtener_catalogo_mapas, VACIO


def obtener_celdas_libres(tablero: List[List[int]], pos_salida: Tuple[int, int]) -> List[Tuple[int, int]]:
    celdas_libres = []
    for f in range(len(tablero)):
        for c in range(len(tablero[0])):
            if tablero[f][c] == VACIO and (f, c) != pos_salida:
                celdas_libres.append((f, c))
    return celdas_libres


def generar_agentes_y_fuegos_aleatorios(celdas_libres: List[Tuple[int, int]], 
                                       cant_agentes: int, 
                                       cant_fuegos: int = 4) -> Tuple[List[Agente], List[Tuple[int, int]]]:
 
    # Proteger si la densidad requerida supera la capacidad del mapa
    limite_capacidad = len(celdas_libres) - cant_fuegos
    if cant_agentes > limite_capacidad:
        print(f"  [!] Advertencia: Tablero al límite. Reduciendo agentes de {cant_agentes} a {limite_capacidad}.")
        cant_agentes = limite_capacidad

    # Selección aleatoria sin reemplazo para garantizar exclusividad de casilla
    seleccionadas = random.sample(celdas_libres, cant_agentes + cant_fuegos)
    pos_agentes = seleccionadas[:cant_agentes]
    pos_fuegos = seleccionadas[cant_agentes:]
    
    agentes = [Agente(id_agente=i + 1, pos_inicial=pos) for i, pos in enumerate(pos_agentes)]
    return agentes, pos_fuegos


def ejecutar_benchmark(iteraciones: int = 50, cant_agentes: int = 150, cant_fuegos_azar: int = 4):
    catalogo_mapas = obtener_catalogo_mapas()
    planificador_ga = PlanificadorGenetico(tam_poblacion=30, longitud_cromosoma=25, generaciones=30)
    
    algoritmos: Dict[str, Callable] = {
        "BFS": breadth_first_search,
        "UCS": uniform_cost_search,
        "Greedy": greedy_best_first_search,
        "A*": a_star_search,
        "Genetic": planificador_ga.genetic_algorithm_search
    }

    datos_crudos = []

    print("=" * 90)
    print(f"INICIANDO BENCHMARKING ({iteraciones} iteraciones | {cant_agentes} agentes | {cant_fuegos_azar} fuegos extra)")
    print("=" * 90)

    for info_mapa in catalogo_mapas:
        nombre_mapa = info_mapa["nombre"]
        tablero_base = info_mapa["tablero"]
        pos_salida = info_mapa["salida"]
        
        celdas_libres = obtener_celdas_libres(tablero_base, pos_salida)

        for nombre_algo, funcion_busqueda in algoritmos.items():
            print(f"-> Procesando: [{nombre_mapa}] con [{nombre_algo}]...")

            for it in range(iteraciones):
                random.seed(it + 2026 + len(nombre_algo))
                
                agentes, fuegos_adicionales = generar_agentes_y_fuegos_aleatorios(
                    celdas_libres, cant_agentes=cant_agentes, cant_fuegos=cant_fuegos_azar
                )

                entorno = Entorno(
                    matriz_tablero=tablero_base, 
                    pos_salida=pos_salida, 
                    k_propagacion_fuego=3, 
                    penalizacion_alfa=1.5
                )
                
                fuegos_totales = list(set(info_mapa["fuegos_iniciales"] + fuegos_adicionales))
                entorno.agregar_fuego_inicial(fuegos_totales)

                res = ejecutar_simulacion(entorno, agentes, funcion_busqueda, turnos_maximos=300)

                datos_crudos.append({
                    "mapa": nombre_mapa,
                    "algoritmo": nombre_algo,
                    "iteracion": it + 1,
                    "tasa_supervivencia": res["tasa_supervivencia"] * 100.0,
                    "tiempo_despeje": res["tiempo_despeje"]
                })

    df_crudos = pd.DataFrame(datos_crudos)
    df_crudos.to_csv("benchmark_datos_crudos.csv", index=False)
    
    # Procesar métricas agregadas
    datos_resumen = []
    for (nombre_mapa, nombre_algo), grupo in df_crudos.groupby(["mapa", "algoritmo"]):
        tasas = grupo["tasa_supervivencia"].values
        tiempos_validos = grupo["tiempo_despeje"].dropna().values

        datos_resumen.append({
            "Mapa": nombre_mapa,
            "Algoritmo": nombre_algo,
            "Supervivencia Media (%)": round(float(np.mean(tasas)), 2),
            "Supervivencia Desv. Est.": round(float(np.std(tasas)), 2),
            "Turnos Media": round(float(np.mean(tiempos_validos)), 2) if len(tiempos_validos) > 0 else np.nan,
            "Turnos Desv. Est.": round(float(np.std(tiempos_validos)), 2) if len(tiempos_validos) > 0 else np.nan,
            "Turnos Mín": int(np.min(tiempos_validos)) if len(tiempos_validos) > 0 else np.nan,
            "Turnos Máx": int(np.max(tiempos_validos)) if len(tiempos_validos) > 0 else np.nan,
            "Evacuaciones Exitosas": len(tiempos_validos)
        })

    df_resumen = pd.DataFrame(datos_resumen)
    df_resumen.to_csv("benchmark_resumen.csv", index=False)
    
    print("\n" + "=" * 100)
    print("TABLA DE RESULTADOS DE BENCHMARKING")
    print("=" * 100)
    print(df_resumen.to_string(index=False))


if __name__ == "__main__":
    ejecutar_benchmark(iteraciones=200, cant_agentes=150, cant_fuegos_azar=4)