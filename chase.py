import gamelib
 
import random
 
 
ALTO_JUEGO = 20
ANCHO_JUEGO = 20
JUGADOR = 'J'
OBSTACULO = 'X'
ROBOT = 'R'
TERMINADO = 'T'
VACIO = 'O'
CANTIDAD_DE_ROBOTS = 10
QUIETO = (0, 0)
ARRIBA = (0, 1)
ABAJO = (0, -1)
DERECHA = (1, 0)
IZQUIERDA = (-1, 0)
ARRIBA_DERECHA = (1, 1)
ARRIBA_IZQUIERDA = (-1, 1)
ABAJO_DERECHA = (1, -1)
ABAJO_IZQUIERDA = (-1, -1)
 
def crear_grilla():
    grilla = []    
    for c in range(ALTO_JUEGO):
        fila = []
        for b in range(ANCHO_JUEGO):
            fila.append(VACIO)
        grilla.append(fila)
    return grilla
 
def ubicar_piezas():
    x = random.randrange(0, ANCHO_JUEGO)
    y = random.randrange(0, ALTO_JUEGO)
    jugador = (x, y)
    robots = []
    for cantidad_de_robots in range(CANTIDAD_DE_ROBOTS):
        x = random.randrange(0, ANCHO_JUEGO)
        y = random.randrange(0, ALTO_JUEGO)
        robot = (x, y)
        robots.append(robot)
    return jugador, robots
 
        
    
def inicializar_juego(jugador, robots, grilla):
    for x, y in robots:
        grilla[y][x] = ROBOT
    grilla[jugador[1]][jugador[0]] = JUGADOR
    return grilla
    
    
 
def terminado(juego):
    return juego[0][0] == TERMINADO
 
 
 
def encontrar_jugador(juego):
    for fila in range(ALTO_JUEGO):
        for columna in range(ANCHO_JUEGO):
            if juego[fila][columna] == JUGADOR:
                return (columna, fila)
            
def encontrar_robots(juego):
    robots = []
    for fila in range(ALTO_JUEGO):
        for columna in range(ANCHO_JUEGO):
            if juego[fila][columna] == ROBOT:
                robots.append((columna, fila))
    return robots
            
 
    
def reconocer_movimiento_jugador(jugador, x, y):
    if jugador[0] < x and jugador[1] < y:
        return ARRIBA_DERECHA
    elif jugador[0] > x and jugador[1] < y:
        return ARRIBA_IZQUIERDA
    elif jugador[0] < x and jugador[1] > y:
        return ABAJO_DERECHA
    elif jugador[0] > x and jugador[1] > y:
        return ABAJO_IZQUIERDA
    elif jugador[0] < x:
        return DERECHA
    elif jugador[0] > x:
        return IZQUIERDA
    elif jugador[1] < y:
        return ARRIBA
    elif jugador[1] > y:
        return ABAJO
    elif jugador[0] == x and jugador[1] == y:
        return QUIETO
    
 
 
 
def mover_jugador(jugador, partida, movimiento):
    posicion_x, posicion_y = jugador
    movimiento_x, movimiento_y = movimiento
 
    if partida[posicion_y + movimiento_y][posicion_x + movimiento_x] == ROBOT:
        partida[posicion_y][posicion_x] = VACIO
        partida[0][0] = TERMINADO
        return partida
    
    elif partida[posicion_y + movimiento_y][posicion_x + movimiento_x] == VACIO:
        partida[posicion_y + movimiento_y][posicion_x + movimiento_x] = JUGADOR
        partida[posicion_y][posicion_x] = VACIO
        return partida
    
    elif partida[posicion_y + movimiento_y][posicion_x + movimiento_x] == OBSTACULO and partida[posicion_y + movimiento_y + 1][posicion_x + movimiento_x + 1] == VACIO and (movimiento != ARRIBA_DERECHA or movimiento != ARRIBA_IZQUEIRDA or  movimiento != ABAJO_DERECHA or  movimiento != ABAJO_IZQUIERDA):
        partida[posicion_y + movimiento_y + movimiento_y][posicion_x + movimiento_x + movimiento_x] = OBSTACULO
        partida[posicion_y + movimiento_y][posicion_x + movimiento_x] = JUGADOR
        partida[posicion_y][posicion_x] = VACIO       
        return partida
    
    return partida
        
   
    
 
 
def reconocer_movimientos_robots(jugador, robots):
    objetivo_x, objetivo_y = jugador
    movimientos = []
    for posicion_x, posicion_y in robots:
        if posicion_x < objetivo_x and posicion_y < objetivo_y:
            movimientos.append(ARRIBA_DERECHA)
        elif posicion_x > objetivo_x and posicion_y < objetivo_y:
            movimientos.append(ARRIBA_IZQUIERDA)
        elif posicion_x < objetivo_x and posicion_y > objetivo_y:
            movimientos.append(ABAJO_DERECHA)
        elif posicion_x > objetivo_x and posicion_y > objetivo_y:
            movimientos.append(ABAJO_IZQUIERDA)
        elif posicion_x < objetivo_x:
            movimientos.append(DERECHA)
        elif posicion_x > objetivo_x:
            movimientos.append(IZQUIERDA)
        elif posicion_y < objetivo_y:
            movimientos.append(ARRIBA)
        elif posicion_y > objetivo_y:
            movimientos.append(ABAJO)
    return movimientos
 
 
 
 
 
def mover_robots(robots, movimientos_robots, partida):
    posiciones_viejas = robots
    posiciones_nuevas = []
 
    
    for turno in range(len(robots)):
        posicion_x, posicion_y = robots[turno]
        movimiento_x, movimiento_y = movimientos_robots[turno]
        posiciones_nuevas.append((posicion_x + movimiento_x, posicion_y + movimiento_y))
        
    for posicion_x, posicion_y in posiciones_viejas:
        partida[posicion_y][posicion_x] = VACIO
        
    for posicion_x, posicion_y in posiciones_nuevas:
        if partida[posicion_y][posicion_x] == ROBOT or partida[posicion_y][posicion_x] == OBSTACULO:
            partida[posicion_y][posicion_x] = OBSTACULO
            
        elif partida[posicion_y][posicion_x] == JUGADOR:
            partida[posicion_y][posicion_x] = ROBOT
            partida[0][0] = TERMINADO
            
        else:
            partida[posicion_y][posicion_x] = ROBOT
            
    return partida
 
 
 
def robots_chocados(posicion, partida, movimientos):
    robots_chocados = []
    posicion_x, posicion_y = posicion
    
    for movimiento_x, movimiento_y in movimientos:
        if partida[posicion_y - movimiento_y][posicion_x - movimiento_x] == ROBOT:
            robots_chocados.append((posicion_x - movimiento_x, posicion_y - movimiento_y))
    return robots_chocados
 
 
 
def teletransportar(jugador, partida):
    x = random.randrange(0, ANCHO_JUEGO)
    y = random.randrange(0, ALTO_JUEGO)
    
    if partida[y][x] == ROBOT or partida[y][x] == OBSTACULO:
        partida[0][0] = TERMINADO
        
    else:
        partida[jugador[1]][jugador[0]] = VACIO
        partida[y][x] = JUGADOR
        
        
    return partida
    
 
 
def main():
    grilla = crear_grilla()
    jugador, robots = ubicar_piezas()
    partida = inicializar_juego(jugador, robots, grilla)
    gamelib.resize(ANCHO_JUEGO * 50, ALTO_JUEGO * 50)
    
    if gamelib.is_alive():
        gamelib.draw_begin()
        for linea in range(ALTO_JUEGO):
            for columna in range(ANCHO_JUEGO):
                if partida[linea][columna] == VACIO:
                    gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                    
                if partida[linea][columna] == JUGADOR:
                    gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                    gamelib.draw_image('img/jugador.gif', (columna * 50), (linea * 50))
                    
                if partida[linea][columna] == ROBOT:
                    gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                    gamelib.draw_image('img/robot.gif', (columna * 50), (linea * 50))
                    
                if partida[linea][columna] == OBSTACULO:  
                    gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                    gamelib.draw_image('img/obstaculo.gif', (columna * 50), (linea * 50))
 
                if partida[linea][columna] == TERMINADO:
                    gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
    
        gamelib.draw_end()
    
    while gamelib.is_alive():
        
        
        if not terminado(partida):
        
            ev = gamelib.wait()
            
            if not ev:
                break
 
            if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
                break
 
            
            if ev.type == gamelib.EventType.ButtonPress:
                x, y = (ev.x) // 50 , (ev.y) // 50
                jugador = encontrar_jugador(partida)
                robots = encontrar_robots(partida)
 
                if x < 20 and y < 20:
 
                    movimiento = reconocer_movimiento_jugador(jugador, x, y)
 
                    partida = mover_jugador(jugador, partida, movimiento)
 
                    jugador = encontrar_jugador(partida)
 
 
                    movimientos_robots = reconocer_movimientos_robots(jugador, robots)
 
                    partida = mover_robots(robots, movimientos_robots, partida)
                    
                gamelib.draw_begin()
                for linea in range(ALTO_JUEGO):
                    for columna in range(ANCHO_JUEGO):
                        if partida[linea][columna] == VACIO:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == JUGADOR:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/jugador.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == ROBOT:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/robot.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == OBSTACULO:  
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/obstaculo.gif', (columna * 50), (linea * 50))
 
                        if partida[linea][columna] == TERMINADO:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            
                gamelib.draw_end()
                            
                
            if ev.type == gamelib.EventType.KeyPress and ev.key == "space":
                
                jugador = encontrar_jugador(partida)
                
                robots = encontrar_robots(partida)
                
                partida = teletransportar(jugador, partida)
 
                jugador = encontrar_jugador(partida)
 
                movimientos_robots = reconocer_movimientos_robots(jugador, robots)
            
                partida = mover_robots(robots, movimientos_robots, partida)
 
                
                
                gamelib.draw_begin()
                for linea in range(ALTO_JUEGO):
                    for columna in range(ANCHO_JUEGO):
                        if partida[linea][columna] == VACIO:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == JUGADOR:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/jugador.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == ROBOT:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/robot.gif', (columna * 50), (linea * 50))
                            
                        if partida[linea][columna] == OBSTACULO:  
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            gamelib.draw_image('img/obstaculo.gif', (columna * 50), (linea * 50))
 
                        if partida[linea][columna] == TERMINADO:
                            gamelib.draw_image('img/vacio.gif', (columna * 50), (linea * 50))
                            
                gamelib.draw_end()
        
            
      
        
        else:
            gamelib.draw_begin()
            
            gamelib.draw_rectangle(50, 50, 200, 250)
    
            gamelib.draw_end()
            
        
             
                
gamelib.init(main)