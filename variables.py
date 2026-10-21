"""
Define las constantes globales utilizadas en el juego Hundir la Flota.
Incluye la configuración del tablero, la flota, los estados de las celdas,
las orientaciones de los barcos, el nombre de la IA y la paleta de colores.
"""

# CONFIGURACIÓN DEL TABLERO
# Número de filas y columnas del tablero de juego.
TAMANIO_TABLERO = 10

# CONFIGURACIÓN DE LA FLOTA
# Longitud de los barcos, expresada en número de casillas que ocupan.
BARCO_4_POS = 4
BARCO_3_POS = 3
BARCO_2_POS = 2
BARCO_1_POS = 1

# Cantidad de barcos de cada tamaño que componen la flota.
N_BARCO_4_POS = 1
N_BARCO_3_POS = 2
N_BARCO_2_POS = 3
N_BARCO_1_POS = 4

# ESTADOS DE LAS CELDAS
# Cadenas que identifican el estado de cada celda del tablero.
AGUA = "agua"           # Casilla que no contiene un barco.
BARCO = "barco"         # Casilla ocupada por un barco.
FALLO = "fallo"         # Disparo realizado en una casilla de agua.
IMPACTO = "impacto"     # Disparo que alcanza una casilla ocupada por un barco.

# SÍMBOLOS DE REPRESENTACIÓN DEL TABLERO
# Códigos de formato utilizados para representar visualmente cada estado.
# Los códigos de color y estilo permiten distinguir los elementos en pantalla.
AGUA_SIMBOLO = "[#4C7EB6]~[/]"          # Agua: símbolo ~ en azul.
BARCO_SIMBOLO = "[#E69029]#[/]"         # Barco: símbolo # en mostaza.
FALLO_SIMBOLO = "[bold #6DCCB4]o[/]"    # Fallo: letra o en cian y negrita.
IMPACTO_SIMBOLO = "[bold #FE0000]x[/]"  # Impacto: letra x en rojo y negrita.

# ORIENTACIONES DE LOS BARCOS
# Letras utilizadas para indicar la dirección de colocación de un barco.
NORTE = "N"
SUR = "S"
ESTE = "E"
OESTE = "O"

# IDENTIFICACIÓN DE LA INTELIGENCIA ARTIFICIAL
# Nombre asignado a la IA que participa en la partida.
IA_NOMBRE = "Maelstrom"

# PALETA DE COLORES
# Códigos hexadecimales de los colores empleados en la interfaz del juego.
MOSTAZA ="#E69029"
CIAN = "#6DCCB4"
CELESTE = "#BAE8DE"
ROJO = "#FE0000"
AZUL_CLARO = "#4C7EB6"
AGUAMARINA = "#527C70"