import random
import numpy as np
import matplotlib.pyplot as plt

def normalizar_vector(vector):
    suma = sum(vector)
    vector_normalizado = [valor / suma for valor in vector]
    return vector_normalizado


def crear_poblacion(num_individuos, contador_movimientos):
    poblacion = []

    for _ in range(num_individuos):
        cromosoma = creacion_cromosomas(8, contador_movimientos)
        poblacion.append(cromosoma)

    return poblacion


def creacion_cromosomas(num_genes, contador_movimientos):
    # Genera las probabilidades aleatorias
    probabilidades = [random.random() for _ in range(num_genes)]

    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)

    # Crea el cromosoma con probabilidades aleatorias, contador de movimientos y posición actual
    cromosoma = {
        "genes": probabilidades,
        "contador_movimientos": contador_movimientos,
        "posicion_actual": (
            0,
            0,
        ),  # Inicialmente todos los individuos están en la posición (0, 0)
    }

    return cromosoma

def plot_cuadricula(poblacion):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos
    pasos_maximos = poblacion[0]['contador_movimientos']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Cuadrícula")
 
    ax.set_xticks(np.arange(tamano_tablero+1)-0.5, minor=True)
    ax.set_yticks(np.arange(tamano_tablero+1)-0.5, minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

    plt.xlabel('Columna')
    plt.ylabel('Fila')

    plt.ion()

    cuadricula = np.zeros((tamano_tablero, tamano_tablero))

    for i, individuo in enumerate(poblacion):
        cuadricula[i][0] = i + 1
        individuo['posiciones'] = [(i, 0)]

    img = ax.matshow(cuadricula, cmap="Blues")
    plt.draw()
    plt.pause(0.1)

    for paso in range(1, poblacion[0]['contador_movimientos']+1):
        print(f"Paso {paso}:")
        for i, individuo in enumerate(poblacion):
            movimientos = ['sur', 'este', 'oeste', 'noreste', 'noroeste', 'sureste', 'suroeste', 'mantener']
            probabilidades = normalizar_vector(individuo['genes'])
            movimiento = np.random.choice(movimientos, p=probabilidades)

            posicion_actual = individuo['posiciones'][-1]

            nueva_fila, nueva_columna = posicion_actual

            if nueva_columna == 0:
                if movimiento == 'oeste':
                    movimiento = 'este'
                elif movimiento == 'noroeste':
                    movimiento = 'noreste'
                elif movimiento == 'suroeste':
                    movimiento = 'sureste'

            if nueva_columna == tamano_tablero - 1:
                movimiento = 'mantener'

            if movimiento == 'sur':
                nueva_fila -= 1
                if nueva_fila < 0:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'este':
                nueva_columna += 1
                if nueva_columna >= tamano_tablero:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'oeste':
                nueva_columna -= 1
                if nueva_columna < 0:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'noreste':
                nueva_fila -= 1
                nueva_columna += 1
                if nueva_fila < 0 or nueva_columna >= tamano_tablero:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'noroeste':
                nueva_fila -= 1
                nueva_columna -= 1
                if nueva_fila < 0 or nueva_columna < 0:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'sureste':
                nueva_fila += 1
                nueva_columna += 1
                if nueva_fila >= tamano_tablero or nueva_columna >= tamano_tablero:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'suroeste':
                nueva_fila += 1
                nueva_columna -= 1
                if nueva_fila >= tamano_tablero or nueva_columna < 0:
                    movimiento = 'mantener'
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == 'mantener':
                nueva_fila, nueva_columna = posicion_actual

            if cuadricula[nueva_fila][nueva_columna] != 0:
                movimiento = 'mantener'
                nueva_fila, nueva_columna = posicion_actual

            individuo['posiciones'].append((nueva_fila, nueva_columna))

            if nueva_columna != tamano_tablero - 1:
                individuo['contador_movimientos'] -= 1

        cuadricula = np.zeros((tamano_tablero, tamano_tablero))

        for i, individuo in enumerate(poblacion):
            fila, columna = individuo['posiciones'][-1]
            cuadricula[fila][columna] = i + 1
        
        img.set_data(cuadricula)
        
        plt.draw()
        plt.pause(0.1)

    plt.close()

    for individuo in poblacion:
        individuo['posicion_actual'] = individuo['posiciones'][-1]

    seleccion = seleccion_padres(poblacion, pasos_maximos, tamano_tablero)
    return seleccion




def seleccion_padres(poblacion, pasos_maximos, tamano_tablero):
    gen_prueba = [
        {"contador_movimientos": pasos_maximos + 1, "posicion_actual": (0, 0), "id": 0}
    ]
    Mejores_individuos = [gen_prueba[0], gen_prueba[0]]

    print("INDIVIDUOS QUE LLEGARON AL FINAL")
    print("================================")
    for i, individuo in enumerate(poblacion):
        individuo["id"] = i + 1
        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            if (
                individuo["contador_movimientos"]
                < Mejores_individuos[0]["contador_movimientos"]
            ):
                Mejores_individuos[1] = Mejores_individuos[0]
                Mejores_individuos[0] = individuo

            elif (
                individuo["contador_movimientos"]
                < Mejores_individuos[1]["contador_movimientos"]
            ):
                Mejores_individuos[1] = individuo

    print("================================")
    for i, individuo in enumerate(poblacion):
        print(f"individuo {i}, posicion {individuo['posicion_actual']}")

    print("================================")

    if Mejores_individuos[1]["contador_movimientos"] == pasos_maximos + 1:
        return "Ningún individuo llegó al final"

    elif Mejores_individuos[1]["contador_movimientos"] != pasos_maximos + 1:
        print(
            f"MEJORES INDIVIDUOS \n 1er lugar : {Mejores_individuos[0]['id']}, posicion{Mejores_individuos[0]['posicion_actual']}, contador pasos {pasos_maximos - Mejores_individuos[0]['contador_movimientos']} \n 2do lugar : {Mejores_individuos[1]['id']}, posicion{Mejores_individuos[1]['posicion_actual']}, contador pasos {pasos_maximos - Mejores_individuos[1]['contador_movimientos']}"
        )
        return Mejores_individuos

##############################################################################################################
def funcionamiento_principal(Cantidad_generaciones, Cantidad_Individuos,cantidad_movimientos): ## def Obtener2padres():
 Generacion_Actual = 0
 while(Generacion_Actual<Cantidad_generaciones):    
    while True:
        poblacion = crear_poblacion(Cantidad_Individuos,cantidad_movimientos)  # Ejemplo con 10 individuos y 10 movimientos
        resultado = plot_cuadricula(poblacion)
        Generacion_Actual+=1
        if resultado !="Ningún individuo llegó al final" or Generacion_Actual==Cantidad_generaciones:
            break
    print("RESULTADO DE LA SELECCIÓN DE PADRES")
    print("==================================")
    print(resultado)
    print("==================================")
    #nueva_poblacion = reproduccion(resultado) # resultados lleva los 2 mejores individuos
     ### TODO LO DEMAS ####
     
    Generacion_Actual+=1
    return 0


#funcionamiento_principal(40,20,70) # 40 generaciones, 20 individuos, 70 pasos
asd = funcionamiento_principal(40,20,25)

#PRUEBA = funcionamiento_principal(40,20,70)