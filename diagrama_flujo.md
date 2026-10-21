# Diagrama de flujo funcional — Hundir la Flota

## 1. Inicio y preparación de la partida

En primer lugar, se muestran las instrucciones, se crean los jugadores y se preparan los tableros con sus flotas.

```mermaid
flowchart TD
    A([Inicio]) --> B[Mostrar instrucciones]
    B --> C[Crear jugador humano y ordenador]
    C --> D[Crear los tableros]
    D --> E[Colocar aleatoriamente ambas flotas]
    E --> F[Mostrar los tableros iniciales]
```

## 2. Selección del turno y del disparo

Cuando la partida está preparada, se comprueba si quedan barcos a flote y se determina quién debe disparar.

```mermaid
flowchart TD
    A{¿Ambas flotas siguen a flote?}
    A -- Sí --> B[Determinar quién tiene el turno]
    B --> C{¿Turno humano u ordenador?}
    C -- Humano --> D[Introducir fila y columna]
    D --> E{¿Ha escrito SALIR?}
    E -- Sí --> F([Fin por abandono])
    E -- No --> G[Validar las coordenadas]
    C -- Ordenador --> H[Elegir al azar una casilla disponible]
    G --> I[Resolver el disparo]
    H --> I
```

## 3. Resolución del disparo

El resultado del disparo determina qué se registra en el tablero y si el jugador conserva el turno.

```mermaid
flowchart TD
    A[Resolver el disparo] --> B{¿Qué ha ocurrido?}
    B -- Agua --> C[Registrar el fallo]
    C --> D[Cambiar de turno]
    B -- Tocado --> E[Registrar el impacto]
    E --> F[El mismo jugador conserva el turno]
    B -- Hundido --> G[Registrar el impacto y el barco hundido]
    G --> H[Marcar como agua las casillas adyacentes sin explorar]
    H --> F
    D --> I[Actualizar y mostrar los tableros]
    F --> I
```

## 4. Comprobación del final de la partida

Después de cada disparo se vuelven a mostrar los tableros y se comprueba si alguna flota ha sido destruida.

```mermaid
flowchart TD
    A[Actualizar y mostrar los tableros] --> B{¿Ambas flotas siguen a flote?}
    B -- Sí --> C[Continuar la partida y seleccionar el siguiente disparo]
    C --> D[Resolver el disparo]
    B -- No --> E{¿Qué jugador conserva su flota?}
    E -- Humano --> F[Mostrar victoria del jugador]
    E -- Ordenador --> G[Mostrar derrota del jugador]
    F --> H([Fin])
    G --> H
```

## 5. Flujo principal completo

```mermaid
flowchart TD
    A([Inicio]) --> B[Mostrar instrucciones y crear los jugadores]
    B --> C[Crear tableros y colocar ambas flotas aleatoriamente]
    C --> D[Mostrar los tableros iniciales]
    D --> E{¿Ambas flotas siguen a flote?}

    E -- Sí --> F[Determinar quién tiene el turno]
    F --> G{¿Turno humano u ordenador?}
    G -- Humano --> H[Introducir fila y columna]
    H --> I{¿Ha escrito SALIR?}
    I -- Sí --> J([Fin por abandono])
    I -- No --> K[Validar las coordenadas]
    G -- Ordenador --> L[Elegir una casilla disponible al azar]
    K --> M[Resolver el disparo en el tablero rival]
    L --> M

    M --> N{¿Resultado del disparo?}
    N -- Agua --> O[Registrar el fallo y cambiar de turno]
    N -- Tocado --> P[Registrar el impacto y conservar el turno]
    N -- Hundido --> Q[Registrar el impacto y marcar aguas adyacentes]
    Q --> P
    O --> R[Actualizar y mostrar los tableros]
    P --> R
    R --> E

    E -- No --> S{¿Qué jugador conserva su flota?}
    S -- Humano --> T[Mostrar victoria del jugador]
    S -- Ordenador --> U[Mostrar derrota del jugador]
    T --> V([Fin])
    U --> V
```

## 6. Cómo se reparten las responsabilidades en el código
### 6.1. Vista general de los archivos

```mermaid
flowchart TD
    MAIN[main.py<br/>Coordina la partida] --> JUG[clases.py<br/>Jugador, Ordenador y Tablero]
    MAIN --> FUNC[funciones.py<br/>Instrucciones y resultado del disparo]
    JUG --> VAR[variables.py<br/>Reglas y constantes]
    FUNC --> VAR
    MAIN --> RICH[Rich<br/>Presenta paneles y tableros en terminal]
```


- **`main.py`**: pone en marcha el juego, crea los participantes, organiza los turnos y decide cuándo termina la partida.
- **`clases.py`**: contiene los objetos que representan el tablero y a los participantes.
- **`funciones.py`**: contiene funciones auxiliares que no pertenecen a una clase concreta, como mostrar las instrucciones y determinar si un barco ha sido tocado o hundido.
- **`variables.py`**: reúne valores compartidos, como el tamaño del tablero, la flota, los símbolos y las orientaciones.
- **`Rich`**: biblioteca externa que mejora la presentación visual de los mensajes en la terminal.

### 6.2. Clases

```mermaid
classDiagram
    class Tablero {
        tamanio
        estados
        tablero
        
        guardar_texto_filas_tablero(ocultar_barcos = False)
        colocar_barco(fila, columna, tamanio_barco, orientacion)
        marcar_impacto(fila, columna)
        marcar_fallo(fila, columna)
    }

    class Jugador {
        nombre
        tablero_defensa
        tablero_ataque
        flota 
        flota_colocada
        barcos_contador
        vidas
        
        colocar_flota()
        realizar_disparo()
        recibir_disparo(fila, columna)
        anotar_ataque_realizado(fila, columna, respuesta, flota_rival)
        anotar_aguas_barco_hundido(flota_rival)
        sigue_vivo()
    }

    class Ordenador {
        realizar_disparo()
    }

    Ordenador --|> Jugador : hereda de
    Jugador *-- Tablero : tiene dos tableros
```

### 6.3. Cómo colaboran los objetos durante un disparo

```mermaid
sequenceDiagram
    participant M as main.py
    participant A as Jugador actual
    participant R as Jugador rival
    participant TD as Tablero de defensa del rival
    participant TA as Tablero de ataque del jugador
    participant F as funciones.py

    M->>A: realizar_disparo()
    A-->>M: (fila, columna)
    M->>R: recibir_disparo(fila, columna)
    R->>TD: marcar_impacto() o marcar_fallo()
    R->>F: tocado_o_hundido(fila, columna, flota)
    F-->>R: tocado / hundido
    R-->>M: resultado del disparo
    M->>A: anotar_ataque_realizado(fila, columna, resultado, flota_rival)
    A->>TA: marcar_impacto() o marcar_fallo()
    opt El barco ha sido hundido
        A->>TA: anotar aguas adyacentes sin explorar
    end
    M->>M: mostrar resultado y comprobar si continúa la partida
```
