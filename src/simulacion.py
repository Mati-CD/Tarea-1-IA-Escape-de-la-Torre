from typing import List, Tuple, Dict, Any
from entorno import Entorno, FUEGO
from agente import Agente

def ejecutar_simulacion(entorno: Entorno, agentes: List[Agente], funcion_busqueda, 
                        turnos_maximos: int = 200) -> Dict[str, Any]:
    total_agentes = len(agentes)
    entorno.actualizar_ocupacion(agentes)

    while entorno.turno_actual < turnos_maximos:
        entorno.turno_actual += 1
        
        agentes_activos = [a for a in agentes if a.esta_vivo and not a.ha_escapado]
        if not agentes_activos:
            break

        # Cada agente decide a qué casilla desearía moverse
        intenciones = {a.id: a.decidir_siguiente_movimiento(entorno, funcion_busqueda) for a in agentes_activos}
        posiciones_ocupadas_actuales = {a.pos for a in agentes_activos}
        casillas_reservadas = set()
        movimientos_finales = {}

        for a in agentes_activos:
            deseo = intenciones[a.id]

            # Si es la salida, siempre se permite el ingreso para evacuar
            if deseo == entorno.pos_salida:
                movimientos_finales[a.id] = deseo
                continue

            # Dos agentes quieren entrar a la misma casilla en el mismo turno
            conflicto_destino = deseo in casillas_reservadas
            
            # Quiere entrar a una casilla ocupada por otro agente que no se moverá de ahí
            conflicto_ocupacion = (deseo in posiciones_ocupadas_actuales and deseo != a.pos and intenciones.get(
                next((otro.id for otro in agentes_activos if otro.pos == deseo), None)
            ) == deseo)

            if conflicto_destino or conflicto_ocupacion:
                # Se le deniega el paso: ejecuta la acción de esperar en su casilla actual
                movimientos_finales[a.id] = a.pos
                casillas_reservadas.add(a.pos)
                # Reinserta el paso denegado al frente para intentar avanzar en el próximo turno
                a.camino_planificado.insert(0, deseo)
            else:
                movimientos_finales[a.id] = deseo
                casillas_reservadas.add(deseo)

        for a in agentes_activos:
            a.moverse_a(movimientos_finales[a.id], entorno)

        entorno.actualizar_ocupacion(agentes)

        # Propagación de fuego (cada k turnos)
        if entorno.turno_actual % entorno.k_propagacion_fuego == 0:
            entorno.propagar_fuego()
            for a in agentes_activos:
                if entorno.tablero[a.pos[0]][a.pos[1]] == FUEGO:
                    a.esta_vivo = False

    sobrevivientes = [a for a in agentes if a.ha_escapado]
    tasa_supervivencia = len(sobrevivientes) / total_agentes if total_agentes > 0 else 0.0
    tiempo_despeje = max([a.turnos_activo for a in sobrevivientes]) if sobrevivientes else None

    return {
        "sobrevivientes": len(sobrevivientes),
        "total_agentes": total_agentes,
        "tasa_supervivencia": tasa_supervivencia,
        "tiempo_despeje": tiempo_despeje,
        "turnos_totales": entorno.turno_actual
    }