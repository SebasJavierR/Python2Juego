import terminal
import random
import csv

def procesar_especiales():
    """Esta funcion abre el archivo especiales y extrae la informacion sobre
    los bonos especiales que alli se encuentra para luego devolverla en forma de
    lista de listas.
    """
    informacion = []
    with open("especiales.csv") as especiales_info:
        bono = csv.reader(especiales_info, delimiter = ",")
        for fila in bono:
            informacion.append(fila)
    return informacion

def esta_en(ser_o_obs,i,j):
    """recibe la serpiente o los obstaculos y dos cordenadas y juzga si son iguales a alguna
    de las ubicaciones de la serpiente o de un obstaculo
    """
    for v in range(len(ser_o_obs)):
        if int(ser_o_obs[v][0]) == i and int(ser_o_obs[v][-1]) == j:
            return True
    return False

def display(tablero, mostrar):
    """Esta funcion recibe las medidas del tablero y una matriz para imprimirla linea por linea
    """ 
    for j in range(tablero[0]):
        linea = "."
        for i in range(tablero[-1]):
            linea = linea + str(mostrar[j][i] +".")
        print(linea)
    return

def combinar(tablero,fruta,serpiente,obstaculos,pos_especial):
    """ Esta funcion combina la fruta, la serpiente y los obstaculos
    en un matriz de las dimensiones indicadas por tablero, devuelve la matriz resultante
    """
    matriz = []
    for i in range(tablero[0]): #filas
        fila = []
        for j in range(tablero[-1]): #columnas  
            if esta_en(serpiente,i,j):
                fila.append("#")
            elif esta_en(obstaculos,i,j):
                fila.append("%")
            elif fruta[0] == i and fruta[-1] == j:
                fila.append("*")
            elif pos_especial[0] == i and pos_especial[1] == j:                    
                fila.append(pos_especial[2])
            else:
                fila.append(" ")
        matriz.append(fila)
    return matriz

def nueva_pos(direccion,serpiente): #[Fila,columna] lista
    if direccion == "a":
        nuevo_punto = [serpiente[-1][0] , serpiente[-1][-1] -1]
    if direccion == "d":
        nuevo_punto = [serpiente[-1][0] , serpiente[-1][-1] +1]
    if direccion == "s":
        nuevo_punto = [serpiente[-1][0] +1 , serpiente[-1][-1]]
    if direccion == "w":
        nuevo_punto = [serpiente[-1][0] -1 , serpiente[-1][-1]]
    return nuevo_punto

def imprimir_estado_juego(serpiente, fruta, tablero, victoria, obstaculos,numero_nivel,pos_especial,velocidad,almacen,especiales_procesados):
    """Esta funcion recibe la serpiente, la fruta y el tablero,
    con estos parametros genera un tablero del juego
    """
    mostrar = combinar(tablero,fruta,serpiente,obstaculos,pos_especial)
    terminal.clear_terminal()
    print("")
    print("Nivel: ", numero_nivel)
    print("")
    display(tablero, mostrar)
    print("Muevete con A/S/D/W")
    print("Recuerda cuando uses un modificador especial no podras cambiar de direccion")
    print("")
    print("--INFORMACION--")
    print("La victoria se logra con "+ str(victoria) + " puntos")
    print("La fruta esta en: ", fruta)
    print("El objeto especial esta en: ", pos_especial)
    print("Velocidad: ", velocidad)
    print("Serpiente: ",serpiente)
    print("Obstaculos", obstaculos)
    print("")
    print("--Almacen, Objetos Especiales--")
    print("Simbolo    / Tecla      / Cantidad   / Descripcion")
    for i in range(1,len(especiales_procesados)): 
        print(especiales_procesados[i][0],"         /",especiales_procesados[i][3],"         /",almacen[str(especiales_procesados[i][0])],"         /", especiales_procesados[i][4])

    return

def generar_random(serpiente,tablero,obstaculos,otro_objetivo):
    """Esta funcion recibe la serpiente y el tablero y genera un objetivo
    dentro del tablero y que no coinsida con la serpiente
    """
    while True:
        no = 0
        objetivo = [random.randint(0,tablero[0]-1),random.randint(0,tablero[-1]-1)] # [Fila,Columna]
        for v in range(len(serpiente)):
            if objetivo == serpiente[v]:
                no = 1
        for u in range(len(obstaculos)):
            if objetivo == obstaculos[u]:
                no = 1
        if objetivo[0] == otro_objetivo[0] and objetivo[1] == otro_objetivo[1]: #Evita que se genera la fruta en la misma posicion que un objeto especial y alrevez
            no = 1
        if no == 0:
            break
    return objetivo

def choco_obstaculo(nuevo_punto,obstaculos):
    """Esta funcion recibe el nuevo punto de la serpiente y comprueba si
    se encuentra en la misma casilla que algun obstaculo, de encontrarse, 
    devuelve True, sino False
    """
    for i in range(len(obstaculos)):
        if nuevo_punto == obstaculos[i]:
            return True
    return False

def choco_pared(nuevo_punto,serpiente,tablero):
    """ Esta funcion recibe el nuevo punto, la serpiente y la tabla y comprueba si choco
    contra la pared o no, devuelve verdadero o falso si la situacion se dio o no
    """
    if nuevo_punto[0] > tablero[0]-1 or nuevo_punto[-1] > tablero[-1]-1:
        return True
    if nuevo_punto[0] < 0 or nuevo_punto[-1] < 0:
        return True
    return False

def choco_ella_misma(nuevo_punto,serpiente):
    """Esta funcion resive el nuevo punto y la serpiente y comprueba si choco con si misma,
    devuelve verdadero o falso si la situacion se dio o no
    """
    
    for h in range(len(serpiente)-1):
        if nuevo_punto[0] == serpiente[h][0] and nuevo_punto[-1] == serpiente[h][-1]:
            return True
    return False

def choco(nuevo_punto,serpiente,tablero,obstaculos):
    """Esta funcion recibe el nuevo punto, la serpiente, el tablero y los obstaculos
    y hace de menu para las funciones que comprueban si choco con la pared
    la serpiente o con si misma, para devolver verdadero o falso si dan estas
    situaciones
    """
    if choco_pared(nuevo_punto,serpiente,tablero) or choco_ella_misma(nuevo_punto,serpiente) or choco_obstaculo(nuevo_punto,obstaculos):
        terminal.clear_terminal()
        print("")
        print("La serpiente choco! ")
        print("")
        return True
    return False

def menu(victoria,velocidad,tablero,obstaculos,especiales,numero_nivel):
    """Esta funcion recibe un tablero y la velocidad, con ello 
    funciona como "menu" para el funcionamiento del juego.
    """
    especiales_procesados = procesar_especiales()
    crece = 0
    serpiente = [[tablero[0]//2 , tablero[-1]//2]]
    ultima_direccion = "w"
    otro_objetivo = [-1,-1]
    fruta = generar_random(serpiente,tablero,obstaculos,otro_objetivo)
    pos_especial = generar_random(serpiente,tablero,obstaculos,fruta)
    azar = random.randint(0,len(especiales)-1)
    pos_especial.append(especiales[azar])
    puntuacion = 0
    almacen = {}
    for i in range(1,len(especiales_procesados)):
        almacen[especiales_procesados[i][0]] = 0
    activar_especial = " "
    nueva_direccion = "inicializando"
    while True:

        imprimir_estado_juego(serpiente, fruta, tablero, victoria, obstaculos,numero_nivel,pos_especial,velocidad,almacen,especiales_procesados)
        
        nueva_direccion = terminal.timed_input(velocidad)
        if nueva_direccion != "":
            for j in range(1,len(especiales_procesados)):
                if nueva_direccion[0] == str(especiales_procesados[j][3]):
                    activar_especial = nueva_direccion[0]
        try:
            if nueva_direccion[0] == "w" or nueva_direccion[0] == "a" or nueva_direccion[0] == "s" or nueva_direccion[0] == "d":
                direccion = nueva_direccion[0]
                ultima_direccion = nueva_direccion[0]
            else:
                direccion = ultima_direccion
        except:
            direccion = ultima_direccion
        
        nuevo_punto = nueva_pos(direccion,serpiente)

        for i in range(1,len(especiales_procesados)): 
            if activar_especial == especiales_procesados[i][3] and int(almacen[especiales_procesados[i][0]]) > 0 :
                if "velocidad" == str(especiales_procesados[i][1]):
                    velocidad += float(especiales_procesados[i][2])
                if "largo" == str(especiales_procesados[i][1]):
                    crece += int(especiales_procesados[i][2])
                almacen[especiales_procesados[i][0]] += -1

        activar_especial = " "

        if nuevo_punto == fruta:
            fruta = generar_random(serpiente,tablero,obstaculos,pos_especial)
            puntuacion = puntuacion + 1
            crece += 1

        if nuevo_punto[0] == pos_especial[0] and nuevo_punto[1] == pos_especial[1]:
            almacen[pos_especial[2]] += 1
            pos_especial = generar_random(serpiente,tablero,obstaculos,fruta)
            azar = random.randint(0 , len(especiales)-1)
            pos_especial.append(especiales[azar])


        if choco(nuevo_punto,serpiente,tablero,obstaculos):
            print("Perdiste...")
            print("tu puntuacion fue de", puntuacion)
            return True

        serpiente.append(nuevo_punto)
        if crece < 1:
            serpiente.pop(0)
        if crece >= 1:
            crece -= 1  

        if puntuacion >= victoria:
            print("Felicidades Usted a llegado al objetivo de " + str(victoria) + " puntos, ganaste!")
            break
    return False

def procesar_nivel(numero_nivel):
    """Esta funcion recibe un nivel y devuelve los datos por separado
    del archivo que corresponde a dicho nivel.
    """
    with open("nivel_"+ str(numero_nivel)+".txt") as nivel:
        victoria = nivel.readline()
        victoria = int(victoria.rstrip('\n'))

        velocidad = nivel.readline()
        velocidad = float(velocidad.rstrip('\n')) 

        tablero = nivel.readline()
        tablero = tablero.rstrip('\n')
        tablero = tablero.split("x")
        a , b = tablero
        tablero = int(a) , int(b)

        obstaculos_aux = nivel.readline()
        obstaculos_aux = obstaculos_aux.rstrip('\n')
        obstaculos_aux = obstaculos_aux.split(";")
        obstaculos = []
        for i in range(len(obstaculos_aux)):
            obstaculo = obstaculos_aux[i].split(",")
            a , b = obstaculo
            obstaculo = [int(a) , int(b)]
            obstaculos.append(obstaculo)

        especiales = nivel.readline()
        especiales = especiales.rstrip('\n')
        especiales = especiales.split(",")

    return victoria, velocidad, tablero, obstaculos, especiales


def inicio():
    """Esta funcion sirve como menu de inicio, para elegir el nivel que se desea jugar
    y procesar el archivo del nivel que corresponde.
    """
    terminal.clear_terminal()
    numero_nivel = 1
    while True:
        try:
            victoria, velocidad, tablero, obstaculos, especiales = procesar_nivel(numero_nivel)
            if menu(victoria,velocidad,tablero,obstaculos,especiales,numero_nivel):
                break
            numero_nivel += 1
        except:
            print("No se encontraron mas niveles, reinicie el juego si desea jugar otra vez...")
            break
    return
    

inicio()
