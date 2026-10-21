"""Funciones auxiliares para la lógica y la presentación del juego Hundir la Flota.

Incluye la evaluación de los disparos y la impresión de las instrucciones iniciales.
"""

import string
import time
import variables as var
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Consola de Rich reutilizada para mostrar textos con formato en la terminal.
consola = Console()


def tocado_o_hundido(fila, columna, flota):
    """Determina el resultado de un disparo y actualiza las vidas del barco.

    Args:
        fila: Letra de la fila atacada (A-J).
        columna: Número de la columna atacada (1-10).
        flota: Diccionario con la información y coordenadas de cada barco.

    Returns:
        ``"hundido"`` si el barco se queda sin vidas, ``"tocado"`` si
        todavía conserva alguna, o ``"fallo"`` si no había barco en esa celda.
    """

    # Convertir las coordenadas visibles en índices de la matriz (base cero).
    fila_conv = string.ascii_uppercase.index(fila.upper())
    columna_conv = int(columna) - 1

    impacto = (fila_conv, columna_conv)

    # Comprobar si la coordenada pertenece a alguno de los barcos.
    for barco_id, datos in flota.items():
        if impacto in datos["coordenadas"]:
            # Cada impacto reduce en una unidad las vidas restantes del barco.
            flota[barco_id]["vidas_barco"] -= 1
            
            if flota[barco_id]["vidas_barco"] <= 0:
                return "hundido"
            else:
                return "tocado"
    return "fallo"
    

def instrucciones():
    """Muestra por terminal el saludo, el objetivo y las reglas del juego."""

    # Separar visualmente el panel de bienvenida del contenido anterior.
    print()
    consola.print(
    Panel(
        f"\n[bold {var.CELESTE}]¡ B I E N V E N I D O / A   A   H U N D I R   L A   F L O T A !\n", 
        title="Instrucciones",
        subtitle="by alexadodu",
        expand= False, 
        style= var.CIAN))
    # Pausa breve para que el mensaje de bienvenida pueda leerse.
    time.sleep(1.5)

    # Explicar el objetivo principal y las condiciones básicas de la partida.
    consola.print(
        f"\n\n[bold {var.CIAN}]OBJETIVO[/bold {var.CIAN}]\n"
        f"Hundir todos los barcos del submarino enemigo [bold {var.ROJO}]{var.IA_NOMBRE}[/bold {var.ROJO}]"
        " antes de\nque éste logre destruir toda tu flota."
        )

    consola.print(f"\n[bold {var.CIAN}]EL TABLERO[/bold {var.CIAN}]\nCuadrícula de 10 x 10 (las aguas del océano).\n - Filas: de la A a la J.\n - Columnas: del 1 al 10.\n")

    consola.print(f"[bold {var.CIAN}]TU FLOTA[/bold {var.CIAN}]\n - 1 barco de 4 casillas.\n - 2 barcos de 3 casillas.\n - 3 barcos de 2 casillas.\n - 4 barcos de 1 casilla.\n")

    # Describir las dos fases principales y qué ocurre según el resultado del disparo.
    consola.print(f"[bold {var.CIAN}]CÓMO JUGAR[/bold {var.CIAN}]\n")

    consola.print(
        f"[bold {var.MOSTAZA}]1. FASE DE COLOCACIÓN AUTOMÁTICA:[/bold {var.MOSTAZA}]\n"
        "   El sistema desplegará tu flota de forma [bold]aleatoria[/bold] en el tablero,\n   respetando la regla de no tocarse entre sí.\n"
        )

    consola.print(
        f"[bold {var.MOSTAZA}]2. FASE DE DISPARO:[/bold {var.MOSTAZA}]\n"
        f"   Introduce fila y columna para atacar al [bold {var.ROJO}]{var.IA_NOMBRE}[/bold {var.ROJO}].\n"
        f"     [bold]Impacto ([bold {var.ROJO}]x[/bold {var.ROJO}]):[/bold] ¡Acierto! Has dado en un barco enemigo.\n"
        "        Vuelves a disparar inmediatamente.\n"
        f"     [bold]Agua ([bold {var.CIAN}]o[/bold {var.CIAN}]):[/bold] Fallo. El disparo ha caído al mar.\n"
        f"        Pasa el turno al [bold {var.ROJO}]{var.IA_NOMBRE}[/bold {var.ROJO}].\n"
        )