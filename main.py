"""Punto de entrada del juego Hundir la Flota.

Este módulo coordina el inicio de la partida, los turnos, el procesamiento
 de los disparos, la visualización de los tableros y el anuncio del resultado.
La lógica propia de los tableros y los jugadores se encuentra en clases.py;
las instrucciones y la comprobación de barcos tocados o hundidos, en funciones.py.
"""

import clases
import funciones
import time
import variables as var
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

# Consola de Rich: permite mostrar mensajes con formato, paneles y columnas.
consola = Console()

# Mostrar las reglas antes de iniciar la partida y esperar a que el usuario
funciones.instrucciones()

# confirme que está listo para continuar.
input("Presiona ENTER para comenzar... ")

# Crear los dos participantes: el jugador humano y el ordenador.
# Cada objeto Jugador/Ordenador gestiona sus propios tableros y su flota.
nombre_humano = input("Introduce tu nombre: ")
humano = clases.Jugador(nombre_humano)
ordenador = clases.Ordenador(var.IA_NOMBRE)

# Mensaje de bienvenida personalizado.
consola.print(
    Panel(
        f"[bold {var.CELESTE}]¡Buena suerte, {humano.nombre}! Que tus torpedos sean certeros.[/bold {var.CELESTE}]",
        style=var.CIAN,
        expand=False
        ))
time.sleep(1)

# Colocar aleatoriamente las flotas de ambos participantes.
# El método colocar_flota() se encarga de respetar las reglas de colocación.
humano.colocar_flota()
ordenador.colocar_flota()

print("\nFlotas colocadas con éxito.\n")
time.sleep(1)

# Preparar los tableros iniciales para mostrarlos uno al lado del otro.
# El tablero de defensa del jugador muestra sus propios barcos.
# El tablero de ataque del jugador empieza vacío y no revela la flota rival.
texto_tablero_jugador_inicial = humano.tablero_defensa.guardar_texto_filas_tablero()
texto_tablero_ordenador_inicial = ordenador.tablero_defensa.guardar_texto_filas_tablero(True)
time.sleep(1)

# Crear los paneles visuales de los tableros iniciales.
panel_jugador_inicial = Panel(
    texto_tablero_jugador_inicial, 
    title=f"[bold {var.AGUAMARINA}]TU TABLERO[/bold {var.AGUAMARINA}]", 
    subtitle=f"[{var.AGUAMARINA}]defensa[/{var.AGUAMARINA}]",
    expand=False, 
    border_style= var.AGUAMARINA)
panel_rival_inicial = Panel(
    texto_tablero_ordenador_inicial, 
    title=f"[bold {var.AGUAMARINA}]TABLERO RIVAL[/bold {var.AGUAMARINA}]",
    subtitle=f"[{var.AGUAMARINA}]ataque[/{var.AGUAMARINA}]", 
    expand=False,
    border_style= var.AGUAMARINA)

# Mostrar ambos tableros en paralelo y dejar tiempo para verlos.
consola.print(Columns([panel_jugador_inicial, panel_rival_inicial]))
time.sleep(2)


# Inicializar el control de turnos.
# 'partida' se incrementa cuando hay un fallo; por eso un impacto permite
# al mismo participante volver a disparar.
partida = 0
jugadores_ids = [humano, ordenador]
abandono = False

# Bucle principal: continúa mientras ambos participantes conserven vidas.
while humano.sigue_vivo() and ordenador.sigue_vivo():
    # El resto de la división entre 2 selecciona el jugador del turno actual:
    # índice 0 para el humano e índice 1 para el ordenador.
    turno_actual = partida % 2 # da siempre resultados de 0 (par) y 1 (impar)
    jugador_actual = jugadores_ids[turno_actual]
    rival = jugadores_ids[(turno_actual + 1) % 2]

    # Anunciar de quién es el turno.
    consola.print(
        Panel(
            f"Turno de [bold {var.CELESTE}]{jugador_actual.nombre}[/bold {var.CELESTE}].",
            style= var.AGUAMARINA,
            expand=False
            ))
    time.sleep(1)
    
    # Solicitar las coordenadas del disparo. El método devuelve una tupla
    # (fila, columna), o None si el participante decide abandonar.
    resultado_ataque = jugador_actual.realizar_disparo()

    # Si realizar_disparo() devuelve None, finalizar la ejecución del juego.
    if resultado_ataque is None:
        consola.print(
            Panel(
                f"[bold {var.CELESTE}]Has abandonado la partida.[/bold {var.CELESTE}]\n"
                f"[italic {var.CELESTE}]¡Hasta la próxima, [bold {var.CIAN}]{jugador_actual.nombre}[/bold {var.CIAN}]![/italic {var.CELESTE}]",
                title="Fin de la partida",
                expand=False,
                style= var.AGUAMARINA  
                ))
        print()
        time.sleep(1.5)
        exit()


    # Separar las coordenadas recibidas para procesar el disparo.
    fila, columna = resultado_ataque
    
    # El rival registra el disparo en su tablero de defensa y determina si
    # ha sido agua, un barco tocado o un barco hundido.
    resultado = rival.recibir_disparo(fila, columna)

    # El atacante registra el resultado en su tablero de ataque. Si el barco
    # se ha hundido, este método también anota las aguas adyacentes.
    jugador_actual.anotar_ataque_realizado(fila, columna, resultado, rival.flota_colocada)


    # Mostrar un mensaje diferente según el resultado del disparo.
    if resultado == "tocado":
        if jugador_actual == ordenador:
            # Mensaje cuando la IA alcanza un barco del jugador humano.
            consola.print(
                Panel(
                    f"[bold {var.ROJO}]{jugador_actual.nombre}[/bold {var.ROJO}] ha impactado en [bold]{fila}{columna}[/bold].\n"
                    f"[italic {var.CELESTE}]Tu barco tocado... ¡sigue a flote![/italic {var.CELESTE}]",
                    title= "IMPACTO",
                    expand= False,
                    style= var.MOSTAZA
                ))
            print()       
            time.sleep(1.5)
        elif jugador_actual == humano:
            # Mensaje cuando el jugador humano alcanza un barco rival.
            consola.print(
                Panel(
                    f"[bold {var.CIAN}]{jugador_actual.nombre},[/bold {var.CIAN}] has impactado en [bold]{fila}{columna}[/bold].\n"
                    f"[italic {var.CELESTE}]Barco tocado, pero... ¡sigue a flote![/italic {var.CELESTE}]",
                    title= "IMPACTO",
                    expand= False,
                    style= var.MOSTAZA
                ))
            print()       
            time.sleep(1.5)
        
    elif resultado == "hundido":
        if jugador_actual == ordenador:
            # La IA ha destruido uno de los barcos del jugador humano.
            consola.print(
                Panel(
                    f"[bold {var.ROJO}]¡BARCO TOCADO Y HUNDIDO![/bold {var.ROJO}]\n"
                    f"[italic {var.AZUL_CLARO}]{jugador_actual.nombre}[/italic {var.AZUL_CLARO}] ha enviado un barco tuyo al fondo del mar.",
                    title="HUNDIDO",
                    expand=False,
                    style=var.ROJO
                ))
            time.sleep(1.5)
        elif jugador_actual == humano:
            # El jugador humano ha destruido uno de los barcos de la IA.
            consola.print(
                Panel(
                    f"[bold {var.ROJO}]¡BARCO TOCADO Y HUNDIDO![/bold {var.ROJO}]\n"
                    f"[italic {var.AZUL_CLARO}]{jugador_actual.nombre},[/italic {var.AZUL_CLARO}] has enviado un barco enemigo al fondo del mar.",
                    title="HUNDIDO",
                    expand=False,
                    style=var.ROJO
                ))
            time.sleep(1.5)
        
    else:
        # Si el disparo falla, avanzar el contador para que el turno pase
        # al otro participante.
        partida += 1

        if jugador_actual == ordenador:
            # Mensaje cuando la IA dispara al agua.
            consola.print(
                Panel(
                    f"[bold {var.CIAN}]{jugador_actual.nombre}[/bold {var.CIAN}] ha fallado en [bold]{fila}{columna}[/bold].\n"
                    f"[italic {var.AZUL_CLARO}]Solo agua...[/italic {var.AZUL_CLARO}]",
                    title="AGUA",
                    expand=False,
                    style=var.AZUL_CLARO
                ))
            time.sleep(1.5)

        elif jugador_actual == humano:
            # Mensaje cuando el jugador humano dispara al agua.
            consola.print(
                Panel(
                    f"[bold {var.CIAN}]{jugador_actual.nombre}[/bold {var.CIAN}], has fallado en [bold]{fila}{columna}[/bold].\n"
                    f"[italic {var.AZUL_CLARO}]Solo agua...[/italic {var.AZUL_CLARO}]",
                    title="AGUA",
                    expand=False,
                    style= var.AZUL_CLARO
                ))
            time.sleep(1.5)

    
    # Actualizar la representación de los tableros tras cada disparo.
    # Se muestra el tablero de defensa propio y el registro de ataques del
    # jugador humano; así no se revelan las posiciones reales de la IA.
    texto_tablero_jugador = humano.tablero_defensa.guardar_texto_filas_tablero()
    texto_tablero_ordenador = humano.tablero_ataque.guardar_texto_filas_tablero()   

    # Crear los paneles actualizados de defensa y ataque.
    panel_jugador = Panel(
        texto_tablero_jugador, 
        title="[bold #527C70]TU TABLERO[/bold #527C70]", 
        subtitle="[#527C70]defensa[/#527C70]",
        expand=False, 
        border_style= "#527C70")
    panel_rival = Panel(
        texto_tablero_ordenador, 
        title="[bold #527C70]TABLERO RIVAL[/bold #527C70]", 
        subtitle="[#527C70]ataque[/#527C70]",
        expand=False,
        border_style= "#527C70")

    # Mostrar los dos tableros en paralelo después de cada jugada.
    consola.print(Columns([panel_jugador, panel_rival]))
    time.sleep(1.5)


# Cuando uno de los participantes se queda sin vidas, termina el bucle.
# Comprobar quién sigue vivo permite determinar el resultado de la partida.
if humano.sigue_vivo():
    # Si el jugador humano conserva vidas, ha ganado.
    consola.print(
        Panel(
            f"[bold {var.MOSTAZA}]¡VICTORIA TOTAL![/bold {var.MOSTAZA}]\n\n"
            f"[bold {var.CELESTE}]{humano.nombre},[/bold {var.CELESTE}] has derrotado al [bold]{ordenador.nombre}[/bold].\n"
            f"[italic {var.AZUL_CLARO}]La flota enemiga yace en el fondo del océano.[/italic {var.AZUL_CLARO}]",
            title="VICTORIA",
            subtitle="by alexadodu",
            expand=False,
            style= var.MOSTAZA
        ))
    
elif ordenador.sigue_vivo():
    # Si el ordenador conserva vidas, el jugador humano ha perdido.
    consola.print(
        Panel(
            f"[bold {var.ROJO}]¡DERROTA![/bold {var.ROJO}]\n\n"
            f"[bold {var.CELESTE}]{humano.nombre}[/bold {var.CELESTE}], el [bold {var.ROJO}]{ordenador.nombre}[/bold {var.ROJO}] ha aniquilado tu flota.\n"
            f"[italic {var.AGUAMARINA}]Otra vez será... [/italic {var.AGUAMARINA}]",
            title="DERROTA",
            subtitle="by alexadodu",
            expand=False,
            style= var.ROJO
        ))