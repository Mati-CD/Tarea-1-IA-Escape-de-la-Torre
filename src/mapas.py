from typing import List, Tuple, Dict, Any

# 0: VACIO 
# 1: MURO 
# 2: SALIDA 

def obtener_mapa_1() -> Dict[str, Any]:
    """
    Mapa 1: Cuello de botella y alta densidad.
    Varios pasillos angostos convergen en un único corredor hacia la salida.
    """
    tablero = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2], 
    ]
    return {
        "nombre": "Mapa 1 (Cuello de Botella)",
        "tablero": tablero,
        "salida": (7, 11),
        "fuegos_iniciales": [(0, 0), (0, 1)]
    }


def obtener_mapa_2() -> Dict[str, Any]:
    """
    Mapa 2: Laberinto corporativo y densidad media.
    Salas con accesos limitados e intersecciones ciegas.
    """
    tablero = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2], 
    ]
    return {
        "nombre": "Mapa 2 (Laberinto)",
        "tablero": tablero,
        "salida": (7, 11),
        "fuegos_iniciales": [(0, 6)]
    }


def obtener_mapa_3() -> Dict[str, Any]:
    """
    Mapa 3: Dispersión abierta y baja densidad de obstáculos.
    Espacio diáfano con columnas aisladas que permite diversas rutas alternativas.
    """
    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2], 
    ]
    return {
        "nombre": "Mapa 3 (Dispersión Abierta)",
        "tablero": tablero,
        "salida": (7, 11),
        "fuegos_iniciales": [(0, 0)]
    }


def obtener_catalogo_mapas() -> List[Dict[str, Any]]:
    """Retorna los tres mapas requeridos en una lista indexable."""
    return [obtener_mapa_1(), obtener_mapa_2(), obtener_mapa_3()]