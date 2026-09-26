# Tarea 1: Escape de la Torre - Inteligencia Artificial

## Integrante
* Matías Cuello

## Descripción del Proyecto
Este repositorio contiene la implementación de un sistema de navegación y toma de decisiones para la evacuación de un edificio en llamas. El entorno simula la propagación dinámica del fuego y penaliza la congestión en los pasillos.

Se implementaron cinco algoritmos distribuidos en tres paradigmas de búsqueda:

1. **Búsqueda no informada:** BFS (Anchura) y UCS (Costo Uniforme).
2. **Búsqueda informada:** Greedy Best-First y A* (Heurística Manhattan).
3. **Metaheurística:** Algoritmo Genético.

## Requisitos y Dependencias
Para ejecutar el código, se requiere Python 3.x y las siguientes librerías:

```bash
pip install pygame pandas numpy
```

## Instrucciones de Ejecución

### 1. Visualizador Interactivo (Recomendado)
Permite observar la simulación en tiempo real con una interfaz gráfica en 2D, alternando entre los 3 mapas y los 5 algoritmos.

```bash
python visualizador.py
```

**Controles:**
* `1` a `5`: Cambiar de algoritmo.
* `Espacio`: Pausar/Reanudar simulación.
* `R`: Reiniciar el escenario actual.
* Clic con el ratón en los botones superiores e inferiores para cambiar de mapa o algoritmo.

### 2. Simulación por Consola
Ejecuta una demostración rápida en modo texto de todos los algoritmos sobre el Mapa 1.

```bash
python main.py
```

### 3. Benchmarking Estadístico
Ejecuta las pruebas masivas requeridas para la evaluación (100 iteraciones por mapa y algoritmo con variaciones estocásticas) y genera los archivos `.csv` con los estadísticos descriptivos de supervivencia y tiempos de despeje.

```bash
python benchmark.py
```
