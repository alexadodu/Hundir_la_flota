"""Clases y lógica principal del juego Hundir la Flota.

Incluye la representación del tablero, los jugadores y el comportamiento de la IA.
"""

import string
import random
import variables as var
import funciones


class Tablero:
    """Representa un tablero y permite colocar barcos y registrar disparos."""

    def __init__(self, tamanio = var.TAMANIO_TABLERO):
        """Inicializa un tablero cuadrado con todas sus casillas en estado de agua.

        Args:
            tamanio: Número de filas y columnas del tablero.
        """
        self.tamanio = tamanio

        # Relaciona el estado interno de cada casilla con su símbolo de visualización.
        self.estados = {
            var.AGUA: var.AGUA_SIMBOLO,
            var.BARCO: var.BARCO_SIMBOLO,
            var.FALLO: var.FALLO_SIMBOLO,
            var.IMPACTO: var.IMPACTO_SIMBOLO
        }

        # Construye la matriz del tablero: una lista por fila y una celda por columna.
        self.tablero = []
        for _ in range(self.tamanio):
            linea = []
            for _ in range(self.tamanio):
                linea.append(var.AGUA)
            self.tablero.append(linea)


    def guardar_texto_filas_tablero(self, ocultar_barcos= False):
        """Devuelve el tablero como texto, listo para mostrar en consola.

        Args:
            ocultar_barcos: Si es True, representa los barcos como agua para ocultarlos.

        Returns:
            Cadena con encabezados de filas y columnas y los símbolos de cada casilla.
        """
        # Prepara el encabezado de columnas y el contenido textual del tablero.
        texto_total = " \n"

        numeros = "  "
        for num in range(1, self.tamanio + 1):
            numeros += f" {num}"
        texto_total += f"{numeros}\n"

        # Añade cada fila, identificándola con una letra (A, B, C...).
        for indice_fila, fila in enumerate(self.tablero):
            letra = string.ascii_uppercase[indice_fila]
            texto_fila = f"{letra}  "

            for celda in fila:
                if ocultar_barcos and celda == var.BARCO:
                    simbolo = self.estados[var.AGUA]
                else:
                    simbolo = self.estados[celda]
                texto_fila += f"{simbolo} "
            texto_total += texto_fila + "\n"
        
        return texto_total


    def colocar_barco(self, fila, columna, tamanio_barco, orientacion):
        """Intenta colocar un barco sin salirse del tablero ni tocar otros barcos.

        Las coordenadas recibidas usan índices desde cero. La orientación determina
        cómo se extiende el barco desde la casilla inicial.

        Returns:
            Lista de coordenadas ocupadas si se coloca el barco; False si no es válido.
        """

        # Calcula tamaño del barco
        celdas_barco = []

        # Calcula las coordenadas que ocuparía el barco según su orientación.
        for i in range(tamanio_barco):
            if orientacion == None: # Para barcos de 1 celda
                celdas_barco.append((fila, columna))
            elif orientacion == var.NORTE:
                celdas_barco.append((fila - i, columna))
            elif orientacion == var.SUR:
                celdas_barco.append((fila + i, columna))
            elif orientacion == var.ESTE:
                celdas_barco.append((fila, columna + i))
            elif orientacion == var.OESTE:
                celdas_barco.append((fila, columna - i))

        # Comprueba límites y ocupación; a la vez reúne las casillas vecinas.
        celdas_adyacentes = set()

        for f, c in celdas_barco:
            # determina si está dentro del tablero
            if f in range(0, self.tamanio) and c in range(0, self.tamanio):
                #determina si no hay un barco ya en esas coordenadas
                if self.tablero[f][c] == var.AGUA:
                    # calcula celdas adyacentes 
                    for f_ady in [-1,0,1]:
                        for c_ady in [-1,0,1]:
                            if f_ady != 0 or c_ady != 0:
                                celdas_adyacentes.add((f + f_ady,c + c_ady))                 
                    
                else:
                    return False # ya hay un barco
            else:
                return False # barco fuera del tablero

        # Las casillas del propio barco no cuentan como adyacentes a él mismo.
        celdas_adyacentes -= set(celdas_barco)

        # Comprueba que las celdas adyacentes están dentro del tablero 
        # y si son agua, es decir, que no hay barco
        for x, y in celdas_adyacentes:
            if x in range(0, self.tamanio) and y in range(0, self.tamanio):
                if self.tablero[x][y] == var.BARCO:
                    return False # Barco demasiado cerca

        # Solo modifica el tablero cuando todas las comprobaciones han sido superadas.
        for f_barco, c_barco in celdas_barco:
            self.tablero[f_barco][c_barco] = var.BARCO
        
        return celdas_barco


    def marcar_impacto(self, fila, columna):
        """Marca una casilla como impacto si las coordenadas son válidas.

        La fila se indica con una letra y la columna con un número empezando en 1.
        Devuelve True si se marca la casilla y False si las coordenadas no son válidas.
        """

        # Comprobamos errores por si el usuario introduce letras en vez de números y viceversa
        try:
            fila_conv = string.ascii_uppercase.index(fila.upper())
            columna_conv = int(columna) - 1

            if fila_conv in range(0, self.tamanio) and columna_conv in range(0, self.tamanio):
                self.tablero[fila_conv][columna_conv] = var.IMPACTO
                return True
            else:
                return False

        except (ValueError, TypeError):
            return False

    def marcar_fallo(self, fila, columna):
        """Marca una casilla como fallo si las coordenadas son válidas.

        Devuelve True si se marca la casilla y False si las coordenadas no son válidas.
        """

        # Comprobamos errores por si el usuario introduce letras en vez de números y viceversa
        try:
            fila_conv = string.ascii_uppercase.index(fila.upper())
            columna_conv = int(columna) - 1

            if fila_conv in range(0, self.tamanio) and columna_conv in range(0, self.tamanio):
                self.tablero[fila_conv][columna_conv] = var.FALLO
                return True
            else:
                return False

        except (ValueError, TypeError):
            return False
pass


class Jugador():
    """Representa a un participante humano y contiene su estado de juego."""

    def __init__(self, nombre):
        """Inicializa los tableros, la composición de la flota y las vidas del jugador."""
        self.nombre = nombre
        # El tablero de defensa registra los barcos propios y los disparos recibidos.
        self.tablero_defensa = Tablero()
        # El tablero de ataque registra los disparos realizados contra el rival.
        self.tablero_ataque = Tablero()
        # Claves: cantidad de barcos de cada tipo; valores: longitud de esos barcos.
        self.flota = {
            var.N_BARCO_1_POS: var.BARCO_1_POS,
            var.N_BARCO_2_POS: var.BARCO_2_POS,
            var.N_BARCO_3_POS: var.BARCO_3_POS,
            var.N_BARCO_4_POS: var.BARCO_4_POS
        }

        # Guardará las coordenadas y las vidas restantes de cada barco individual.
        self.flota_colocada = {}
        self.barcos_contador = 0

        # Las vidas totales equivalen al número de casillas ocupadas por la flota.
        self.vidas = 0
        for cantidad_barcos, tamanio_barco in self.flota.items():
            self.vidas += (cantidad_barcos * tamanio_barco)


    def colocar_flota(self):
        """Coloca aleatoriamente toda la flota y registra cada barco individual.

        Si una posición u orientación no es válida, vuelve a intentarlo hasta
        encontrar una colocación permitida.
        """

        for cantidad_barcos, tamanio_barco in self.flota.items():
            for _ in range(cantidad_barcos):
                while True:
                    fila = random.randint(0, var.TAMANIO_TABLERO - 1)
                    columna = random.randint(0, var.TAMANIO_TABLERO - 1)

                    # Los barcos de varias casillas necesitan orientación; los de una, no.
                    if tamanio_barco > 1:
                        orientacion = random.choice([var.NORTE, var.SUR, var.ESTE, var.OESTE])
                    else:
                        orientacion = None

                    barco_colocado_resultado = self.tablero_defensa.colocar_barco(
                        fila, columna, tamanio_barco, orientacion= orientacion)
                    
                    if barco_colocado_resultado:
                        # Registra por separado cada barco para poder detectar cuándo se hunde.
                        self.barcos_contador += 1
                        self.flota_colocada[f"barco{self.barcos_contador}"] = {
                            "coordenadas": barco_colocado_resultado, 
                            "vidas_barco": tamanio_barco
                        }
                        break


    def realizar_disparo(self):
        """Solicita coordenadas de disparo y evita repetir casillas ya atacadas.

        Devuelve (fila, columna) como entrada del usuario o None si solicita salir.
        """

        while True:
            try:
                fila = input("Introduce fila (A, B, C...) o SALIR para abandonar la partida: ").upper().strip()
                if (fila == "SALIR"):
                    return None
                
                columna = input("Introduce columna (1, 2, 3...) o SALIR para abandonar la partida: ")
                if (columna.upper().strip() == "SALIR"):
                    return None

                # Convierte las coordenadas y comprueba si esa casilla ya fue atacada.
                fila_conv = string.ascii_uppercase.index(fila)
                columna_conv = int(columna) - 1

                if fila_conv not in range(0, var.TAMANIO_TABLERO) or \
                    columna_conv not in range(0, var.TAMANIO_TABLERO):
                    print("Coordenadas incorrectas. Inténtalo de nuevo.")
                    continue

                if (self.tablero_ataque.tablero[fila_conv][columna_conv] == var.IMPACTO) or \
                    (self.tablero_ataque.tablero[fila_conv][columna_conv] == var.FALLO):
                    print(f"Ya has disparado en {fila}{columna}. Inténtalo de nuevo.")
                    continue
                else:
                    break
            except (ValueError, TypeError, IndexError):
                print("Coordenadas incorrectas. Inténtalo de nuevo.")
        
        return (fila, columna)


    def recibir_disparo(self, fila, columna):
        """Procesa un disparo rival en el tablero de defensa.

        Si alcanza un barco, registra el impacto, resta una vida al jugador y
        consulta si el barco está tocado o hundido. Si no, registra agua/fallo.
        Devuelve "tocado", "hundido" o "fallo".
        """
        
        if self.tablero_defensa.tablero[string.ascii_uppercase.index(fila.upper())][int(columna) - 1] == var.BARCO:
            
            self.tablero_defensa.marcar_impacto(fila, columna)
            self.vidas -= 1

            resultado = funciones.tocado_o_hundido(fila, columna, self.flota_colocada)
            return resultado
        else:
            self.tablero_defensa.marcar_fallo(fila, columna)
            return "fallo"


    def anotar_aguas_barco_hundido(self, flota_rival):
        """Marca como fallos las casillas adyacentes a los barcos ya hundidos.

        Solo modifica casillas que siguen en estado AGUA, por lo que conserva
        los impactos y fallos que ya estuvieran registrados.
        """

        celdas_barcos = []
        celdas_adyacentes = set()

        # Recopila todas las coordenadas pertenecientes a barcos sin vidas restantes.
        for barco_id, _ in flota_rival.items():
            if flota_rival[barco_id]["vidas_barco"] <= 0:
                for index in range(len(flota_rival[barco_id]["coordenadas"])):
                    celdas_barcos.append(flota_rival[barco_id]["coordenadas"][index])

        # Calcula las ocho casillas vecinas de cada segmento de los barcos hundidos.
        for f, c in celdas_barcos:
                for f_ady in [-1,0,1]:
                    for c_ady in [-1,0,1]:
                        if f_ady != 0 or c_ady != 0:
                            celdas_adyacentes.add((f + f_ady, c + c_ady))

        celdas_adyacentes -= set(celdas_barcos) 

        for fila, col in celdas_adyacentes:
            if fila in range(0, var.TAMANIO_TABLERO) and col in range(0, var.TAMANIO_TABLERO):
                if self.tablero_ataque.tablero[fila][col] == var.AGUA:  # No sobrescribe impactos
                    self.tablero_ataque.tablero[fila][col] = var.FALLO


    def anotar_ataque_realizado(self, fila, columna, respuesta, flota_rival):
        """Actualiza el tablero de ataque con el resultado de un disparo.

        Si el disparo hunde un barco, también marca las casillas adyacentes como
        fallos automáticos.
        """

        if respuesta == "tocado" or respuesta == "hundido":
            self.tablero_ataque.marcar_impacto(fila, columna)
        else:
            self.tablero_ataque.marcar_fallo(fila, columna)

        if respuesta == "hundido":
            self.anotar_aguas_barco_hundido(flota_rival)


    def sigue_vivo(self):
        """Indica si al jugador le queda al menos una casilla de flota sin perder."""
        # True si sigue vivo, False si no
        return self.vidas > 0
pass


class Ordenador(Jugador):
    """Jugador controlado por el ordenador, con disparos aleatorios."""

    def realizar_disparo(self):
        """Elige al azar una casilla que todavía no haya sido atacada.

        Devuelve la fila como letra y la columna como número empezando en 1.
        """

        while True:
            fila = random.randint(0, var.TAMANIO_TABLERO - 1)
            columna = random.randint(0, var.TAMANIO_TABLERO - 1)

            if (self.tablero_ataque.tablero[fila][columna] == var.IMPACTO) or \
                (self.tablero_ataque.tablero[fila][columna] == var.FALLO):
                continue
            else:
                break

        fila = string.ascii_uppercase[fila]
        columna = columna + 1
        return (fila, columna)
pass