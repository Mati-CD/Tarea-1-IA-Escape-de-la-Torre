import sys
import os
import random

# Forzar a Python a reconocer la carpeta 'src'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from entorno import Entorno
from agente import Agente
from simulacion import ejecutar_simulacion
from mapas import obtener_catalogo_mapas, VACIO
from busqueda_informada import a_star_search
from genetico import PlanificadorGenetico


def generar_agentes_y_fuegos_aleatorios(entorno: Entorno, cant_agentes: int = 150, cant_fuegos: int = 4):
    """Identifica celdas libres e instancia agentes y fuegos al azar."""
    celdas_libres = []
    for f in range(entorno.filas):
        for c in range(entorno.columnas):
            if entorno.tablero[f][c] == VACIO and (f, c) != entorno.pos_salida:
                celdas_libres.append((f, c))

    if (cant_agentes + cant_fuegos) > len(celdas_libres):
        cant_agentes = len(celdas_libres) - cant_fuegos

    seleccionadas = random.sample(celdas_libres, cant_agentes + cant_fuegos)
    pos_agentes = seleccionadas[:cant_agentes]
    pos_fuegos = seleccionadas[cant_agentes:]
    
    agentes = [Agente(id_agente=i+1, pos_inicial=pos) for i, pos in enumerate(pos_agentes)]
    return agentes, pos_fuegos


def main():
    print("=" * 60)
    print("   SIMULACIÓN EN TERMINAL: ESCAPE DE LA TORRE (TEST 3 MAPAS)")
    print("=" * 60)
    
    catalogo_mapas = obtener_catalogo_mapas()
    algoritmo_elegido = a_star_search 
    
    for indice, info_mapa in enumerate(catalogo_mapas, start=1):
        print(f"\n--- [PRUEBA {indice}/3] Cargando: {info_mapa['nombre']} ---")

        # Configuración del Entorno
        entorno = Entorno(
            matriz_tablero=info_mapa["tablero"],
            pos_salida=info_mapa["salida"],
            k_propagacion_fuego=3,
            penalizacion_alfa=1.5
        )

        # Generación Estocástica
        cant_agentes = 150
        cant_fuegos_azar = 4
        agentes, fuegos_azar = generar_agentes_y_fuegos_aleatorios(entorno, cant_agentes, cant_fuegos_azar)    
        fuegos_totales = fuegos_azar
        entorno.agregar_fuego_inicial(fuegos_totales)
        
        print(f"Instanciados {len(agentes)} agentes y {len(fuegos_totales)} focos de incendio.")
        print("Iniciando evacuación (Algoritmo: A*)...")
        
        # Ejecución de la Simulación
        resultados = ejecutar_simulacion(entorno, agentes, algoritmo_elegido, turnos_maximos=300)

        # Resultados calculados directamente desde los objetos
        salvados = sum(1 for a in agentes if a.ha_escapado)
        muertos = sum(1 for a in agentes if not a.esta_vivo)
        total = len(agentes)
        tasa = (salvados / total) * 100 if total > 0 else 0.0

        print(f"-> Resultados {info_mapa['nombre']}:")
        print(f"   Total Agentes: {total}")
        print(f"   Salvados: {salvados}")
        print(f"   Bajas (Fuego): {muertos}")
        print(f"   Tasa de Supervivencia: {tasa:.2f}%")
        print(f"   Turnos hasta el final: {resultados.get('tiempo_despeje', 'Límite alcanzado')}")
        print("-" * 60)

if __name__ == "__main__":
    main()