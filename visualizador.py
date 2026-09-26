import sys
import os
import pygame
import random

# Forzar a Python a reconocer la carpeta 'src'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from entorno import Entorno, VACIO, MURO, SALIDA, FUEGO
from agente import Agente
from busqueda_no_informada import breadth_first_search, uniform_cost_search
from busqueda_informada import greedy_best_first_search, a_star_search
from genetico import PlanificadorGenetico
from mapas import obtener_catalogo_mapas

# Colores 
COLOR_FONDO = (25, 25, 30)
COLOR_VACIO = (240, 240, 240)
COLOR_MURO = (50, 50, 55)
COLOR_SALIDA = (46, 204, 113)
COLOR_FUEGO = (231, 76, 60)
COLOR_AGENTE = (52, 152, 219)
COLOR_LINEAS = (200, 200, 200)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON_BASE = (60, 64, 72)
COLOR_BOTON_ACTIVO = (41, 128, 185)
COLOR_BOTON_MAPA_ACTIVO = (142, 68, 173)
COLOR_BOTON_RESALTE = (80, 85, 95)

# Ajustado a 20 para que los mapas de 40x40 (800x800 px) quepan bien en el monitor
TAM_CELDA = 20 
ALTO_BARRA_SUPERIOR = 80
ALTO_PANEL_INFERIOR = 95


def reiniciar_escenario(info_mapa: dict, cant_agentes: int = 150, cant_fuegos: int = 3):
    entorno = Entorno(
        matriz_tablero=info_mapa["tablero"],
        pos_salida=info_mapa["salida"],
        k_propagacion_fuego=3,
        penalizacion_alfa=1.5
    )
    
    # Identificar todas las celdas vacías disponibles
    celdas_libres = []
    for f in range(entorno.filas):
        for c in range(entorno.columnas):
            if entorno.tablero[f][c] == VACIO and (f, c) != entorno.pos_salida:
                celdas_libres.append((f, c))

    # Limitar agentes si el mapa es muy pequeño (protección)
    if (cant_agentes + cant_fuegos) > len(celdas_libres):
        cant_agentes = len(celdas_libres) - cant_fuegos

    # Elegir posiciones aleatorias para agentes Y fuegos al mismo tiempo
    seleccionadas = random.sample(celdas_libres, cant_agentes + cant_fuegos)
    pos_agentes = seleccionadas[:cant_agentes]
    pos_fuegos_azar = seleccionadas[cant_agentes:]

    # Aplicar los fuegos aleatorios
    entorno.agregar_fuego_inicial(pos_fuegos_azar)

    # Crear los agentes en las posiciones estocásticas
    agentes = [Agente(id_agente=i+1, pos_inicial=pos) for i, pos in enumerate(pos_agentes)]
    
    entorno.actualizar_ocupacion(agentes)
    return entorno, agentes


def main():
    pygame.init()
    pygame.font.init()
    fuente = pygame.font.SysFont("Arial", 15, bold=True)
    fuente_chica = pygame.font.SysFont("Arial", 12)
    # Sin fuente micro porque con TAM_CELDA=20 los números ya casi no se leen bien, mejor círculos limpios

    catalogo_mapas = obtener_catalogo_mapas()
    indice_mapa = 0

    planificador_ga = PlanificadorGenetico(tam_poblacion=30, longitud_cromosoma=25, generaciones=30)
    algoritmos = [
        {"nombre": "1. BFS", "funcion": breadth_first_search},
        {"nombre": "2. UCS", "funcion": uniform_cost_search},
        {"nombre": "3. Greedy", "funcion": greedy_best_first_search},
        {"nombre": "4. A*", "funcion": a_star_search},
        {"nombre": "5. Genetic", "funcion": planificador_ga.genetic_algorithm_search}
    ]
    indice_algoritmo = 3

    # Generamos 150 agentes y 4 focos de incendio al azar
    entorno, agentes = reiniciar_escenario(catalogo_mapas[indice_mapa], cant_agentes=150, cant_fuegos=4)

    # Función auxiliar para ajustar la ventana si el mapa cambia de tamaño
    def ajustar_ventana(entorno):
        ancho_req = max(800, entorno.columnas * TAM_CELDA)
        alto_req = ALTO_BARRA_SUPERIOR + (entorno.filas * TAM_CELDA) + ALTO_PANEL_INFERIOR
        return pygame.display.set_mode((ancho_req, alto_req)), ancho_req

    pantalla, ancho = ajustar_ventana(entorno)
    pygame.display.set_caption("Visualizador: Escape de la Torre")

    reloj = pygame.time.Clock()
    en_ejecucion = True
    pausado = True 
    retardo_ms = 400 
    tiempo_ultimo_paso = pygame.time.get_ticks()

    while en_ejecucion:
        tiempo_actual = pygame.time.get_ticks()
        pos_raton = pygame.mouse.get_pos()
        
        # Posición de botones 
        botones_mapas = []
        ancho_btn_mapa = 150
        for i in range(len(catalogo_mapas)):
            botones_mapas.append(pygame.Rect(10 + i * (ancho_btn_mapa + 10), 40, ancho_btn_mapa, 30))

        botones_algoritmos = []
        ancho_btn_algo = (ancho - 20 - (len(algoritmos) - 1) * 6) // len(algoritmos)
        pos_y_algo = ALTO_BARRA_SUPERIOR + (entorno.filas * TAM_CELDA) + 40
        for i in range(len(algoritmos)):
            bx = 10 + i * (ancho_btn_algo + 6)
            botones_algoritmos.append(pygame.Rect(bx, pos_y_algo, ancho_btn_algo, 35))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_r:
                    entorno, agentes = reiniciar_escenario(catalogo_mapas[indice_mapa], 150, 4)
                elif pygame.K_1 <= evento.key <= pygame.K_5:
                    indice_algoritmo = evento.key - pygame.K_1
                    entorno, agentes = reiniciar_escenario(catalogo_mapas[indice_mapa], 150, 4)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, rect in enumerate(botones_mapas):
                    if rect.collidepoint(pos_raton):
                        indice_mapa = i
                        entorno, agentes = reiniciar_escenario(catalogo_mapas[indice_mapa], 150, 4)
                        pantalla, ancho = ajustar_ventana(entorno)
                        break
                for i, rect in enumerate(botones_algoritmos):
                    if rect.collidepoint(pos_raton):
                        indice_algoritmo = i
                        entorno, agentes = reiniciar_escenario(catalogo_mapas[indice_mapa], 150, 4)
                        break

        # Simulación de turnos
        agentes_activos = [a for a in agentes if a.esta_vivo and not a.ha_escapado]
        funcion_actual = algoritmos[indice_algoritmo]["funcion"]

        if not pausado and agentes_activos and (tiempo_actual - tiempo_ultimo_paso >= retardo_ms):
            tiempo_ultimo_paso = tiempo_actual
            entorno.turno_actual += 1

            intenciones = {a.id: a.decidir_siguiente_movimiento(entorno, funcion_actual) for a in agentes_activos}

            posiciones_actuales = {a.pos for a in agentes_activos}
            reservadas = set()
            movimientos_finales = {}

            for a in agentes_activos:
                deseo = intenciones[a.id]
                if deseo == entorno.pos_salida:
                    movimientos_finales[a.id] = deseo
                    continue

                if deseo in reservadas or (deseo in posiciones_actuales and deseo != a.pos and intenciones.get(
                    next((otro.id for otro in agentes_activos if otro.pos == deseo), None)
                ) == deseo):
                    movimientos_finales[a.id] = a.pos
                    reservadas.add(a.pos)
                    a.camino_planificado.insert(0, deseo)
                else:
                    movimientos_finales[a.id] = deseo
                    reservadas.add(deseo)

            # Desplazamientos
            for a in agentes_activos:
                a.moverse_a(movimientos_finales[a.id], entorno)

            entorno.actualizar_ocupacion(agentes)

            # Propagar fuego
            if entorno.turno_actual % entorno.k_propagacion_fuego == 0:
                entorno.propagar_fuego()
                for a in agentes_activos:
                    if entorno.tablero[a.pos[0]][a.pos[1]] == FUEGO:
                        a.esta_vivo = False

        pantalla.fill(COLOR_FONDO)

        # Cabecera superior
        sobrevivientes = sum(1 for a in agentes if a.ha_escapado)
        bajas = sum(1 for a in agentes if not a.esta_vivo)
        activos = len(agentes_activos)

        texto_estado = f"Turno: {entorno.turno_actual} | Activos: {activos} | Salvados: {sobrevivientes} | Bajas: {bajas}"
        pantalla.blit(fuente.render(texto_estado, True, COLOR_TEXTO), (10, 10))

        lbl_pausa = "[PAUSADO]" if pausado else "[CORRIENDO]"
        color_pausa = (241, 196, 15) if pausado else (46, 204, 113)
        pantalla.blit(fuente.render(lbl_pausa, True, color_pausa), (ancho - 110, 10))

        # Botones de Mapas
        for i, (m_info, rect) in enumerate(zip(catalogo_mapas, botones_mapas)):
            color = COLOR_BOTON_MAPA_ACTIVO if i == indice_mapa else (COLOR_BOTON_RESALTE if rect.collidepoint(pos_raton) else COLOR_BOTON_BASE)
            pygame.draw.rect(pantalla, color, rect, border_radius=4)
            if i == indice_mapa:
                pygame.draw.rect(pantalla, (255, 255, 255), rect, 2, border_radius=4)
            txt = fuente_chica.render(f"Mapa {i+1}", True, COLOR_TEXTO)
            pantalla.blit(txt, txt.get_rect(center=rect.center))

        # Tablero central
        desplazamiento_x = (ancho - (entorno.columnas * TAM_CELDA)) // 2
        inicio_y = ALTO_BARRA_SUPERIOR
        
        for f in range(entorno.filas):
            for c in range(entorno.columnas):
                rect = pygame.Rect(desplazamiento_x + c * TAM_CELDA, inicio_y + f * TAM_CELDA, TAM_CELDA, TAM_CELDA)
                tipo = entorno.tablero[f][c]
                col = COLOR_MURO if tipo == MURO else (COLOR_FUEGO if tipo == FUEGO else (COLOR_SALIDA if (f, c) == entorno.pos_salida else COLOR_VACIO))
                pygame.draw.rect(pantalla, col, rect)
                pygame.draw.rect(pantalla, COLOR_LINEAS, rect, 1)

        # Agentes
        for a in agentes:
            if a.esta_vivo and not a.ha_escapado:
                f, c = a.pos
                cx = desplazamiento_x + c * TAM_CELDA + TAM_CELDA // 2
                cy = inicio_y + f * TAM_CELDA + TAM_CELDA // 2
                pygame.draw.circle(pantalla, COLOR_AGENTE, (cx, cy), TAM_CELDA // 2 - 2)

        # Panel Inferior de Algoritmos
        lbl_instrucciones = fuente_chica.render("[Espacio]: Pausa/Reanudar | [R]: Reiniciar (Genera nuevos agentes y fuegos al azar)", True, (180, 180, 180))
        pantalla.blit(lbl_instrucciones, (10, inicio_y + entorno.filas * TAM_CELDA + 12))

        for i, (btn, rect) in enumerate(zip(algoritmos, botones_algoritmos)):
            col = COLOR_BOTON_ACTIVO if i == indice_algoritmo else (COLOR_BOTON_RESALTE if rect.collidepoint(pos_raton) else COLOR_BOTON_BASE)
            pygame.draw.rect(pantalla, col, rect, border_radius=5)
            if i == indice_algoritmo:
                pygame.draw.rect(pantalla, (255, 255, 255), rect, 2, border_radius=5)
            t = fuente_chica.render(btn["nombre"], True, COLOR_TEXTO)
            pantalla.blit(t, t.get_rect(center=rect.center))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()