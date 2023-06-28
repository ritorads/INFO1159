import random
import matplotlib.pyplot as plt



def fitness(cromosoma):
    # Funcion de fitness
    return 0


def normalizar_vector(vector):
    suma = sum(vector)
    vector_normalizado = [valor / suma for valor in vector]
    return vector_normalizado


def creacion_cromosomas_perfectos(num_genes, contador_movimientos): 
    probabilidades = [] # Vector de probabilidades
    for _ in range(num_genes):
        probabilidades.append(0)
    probabilidades[2] = 1    
    # Genera las probabilidades aleatorias
    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)
    
    # Crea el cromosoma con probabilidades aleatorias y contador de movimientos
    cromosoma = {
        'genes': probabilidades,
        'contador_movimientos': contador_movimientos
    }

    return cromosoma

def creacion_cromosomas(num_genes, contador_movimientos): 
    # Genera las probabilidades aleatorias
    probabilidades = [random.random() for _ in range(num_genes)]
    
    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)
    
    # Crea el cromosoma con probabilidades aleatorias y contador de movimientos
    cromosoma = {
        'genes': probabilidades,
        'contador_movimientos': contador_movimientos
    }

    return cromosoma


def crear_poblacion(num_individuos, contador_movimientos):
    poblacion = []

    for _ in range(num_individuos):
        cromosoma = creacion_cromosomas(9, contador_movimientos)
        poblacion.append(cromosoma)

    return poblacion


def seleccion_cromosomas():  # % de probabilidad de que sea seleccionado por fitness
    def probabilidad_acumulada():  # definir p de cada cromosoma
        return 0

    def ultimo_cromosoma_menor_round():
        return 0

    def sacar_padres():  # obtenemos los que tengan mejor fitness
        return 0

    return 0


def cruzar_cromosomas():
    return 0


def mutar_cromosomas():
    return 0


def llena_poblacion():
    return 0


def plot_cuadricula_ESPARTANA(poblacion, titulo):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(titulo)

    # Crear una matriz de cuadrícula vacía
    cuadricula = [[0] * 20 for _ in range(20)]

    # Posicionar los individuos en la primera columna de la cuadrícula sin superponerse
    for i, individuo in enumerate(poblacion):
        fila = i
        cuadricula[fila][0] = i + 1

    # Generar un color aleatorio para los individuos
    colores = ['#0000FF'] * len(poblacion)

    # Iterar por cada paso
    pasos_maximos = poblacion[0]['contador_movimientos']
    for paso in range(pasos_maximos):
        # Limpiar la cuadrícula actual
        cuadricula_actual = [[0] * 20 for _ in range(20)]

        # Mover los individuos y cambiar el color según las reglas establecidas
        for fila in range(20):
            for columna in range(20):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    individuo = poblacion[individuo_id - 1]
                    if columna < 19:
                        if cuadricula[fila][columna + 1] == 0:
                            # Mover el individuo según las probabilidades de movimiento
                            movimientos = ['norte', 'sur', 'este', 'oeste', 'diag_ne', 'diag_no', 'diag_se', 'diag_so', 'no_moverse']
                            pesos = individuo['genes'][:9]  # Tomar los primeros 9 valores del vector de genes
                            movimiento = random.choices(movimientos, weights=pesos, k=1)[0]
                            nueva_fila = fila
                            nueva_columna = columna
                            if movimiento == 'norte':
                                nueva_fila -= 1
                            elif movimiento == 'sur':
                                nueva_fila += 1
                            elif movimiento == 'este':
                                nueva_columna += 1
                            elif movimiento == 'oeste':
                                nueva_columna -= 1
                            elif movimiento == 'diag_ne':
                                nueva_fila -= 1
                                nueva_columna += 1
                            elif movimiento == 'diag_no':
                                nueva_fila -= 1
                                nueva_columna -= 1
                            elif movimiento == 'diag_se':
                                nueva_fila += 1
                                nueva_columna += 1
                            elif movimiento == 'diag_so':
                                nueva_fila += 1
                                nueva_columna -= 1

                            # Evitar salir de los límites de la cuadrícula
                            if nueva_fila >= 0 and nueva_fila <= 19 and nueva_columna >= 0 and nueva_columna <= 19:
                                if cuadricula_actual[nueva_fila][nueva_columna] == 0:
                                    cuadricula_actual[nueva_fila][nueva_columna] = individuo_id
                                else:
                                    # La casilla está ocupada, mantener al individuo en su posición actual
                                    cuadricula_actual[fila][columna] = individuo_id
                            else:
                                # El individuo ha llegado al final de la cuadrícula
                                cuadricula_actual[fila][columna] = individuo_id
                        elif columna == 19:
                            # El individuo ha llegado a la última columna y se queda en su posición
                            cuadricula_actual[fila][columna] = individuo_id
                    else:
                        # El individuo ha llegado al final de la cuadrícula
                        cuadricula_actual[fila][columna] = individuo_id

        # Actualizar la cuadrícula
        cuadricula = cuadricula_actual

        # Actualizar el gráfico
        ax.clear()
        ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=len(poblacion))
        for fila in range(20):
            for columna in range(20):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
        ax.grid(True, color='black', linewidth=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
        plt.pause(0.1)  # Pausa para actualizar la gráfica

    # Cambiar el color de los individuos que han llegado al final a verde
    for fila in range(20):
        for columna in range(20):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                colores[individuo_id - 1] = '#00FF00'  # Cambiar el color a verde

    # Actualizar el gráfico final sin cerrarlo
    ax.clear()
    ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=len(poblacion))
    for fila in range(20):
        for columna in range(20):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
    ax.grid(True, color='black', linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Columna')
    ax.set_ylabel('Fila')
    plt.show()

def plot_cuadricula(poblacion, titulo, pasos_maximos_poblacion):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(titulo)

    # Crear una matriz de cuadrícula vacía
    cuadricula = [[0] * 20 for _ in range(20)]

    # Posicionar los individuos en la primera columna de la cuadrícula sin superponerse
    for i, individuo in enumerate(poblacion):
        fila = i
        cuadricula[fila][0] = i + 1

    # Generar un color aleatorio para los individuos
    colores = ['#0330FF'] * len(poblacion)

    # Iterar por cada paso
    pasos_maximos = pasos_maximos_poblacion
    for paso in range(pasos_maximos):
        # Limpiar la cuadrícula actual
        cuadricula_actual = [[0] * 20 for _ in range(20)]

        # Mover los individuos y cambiar el color según las reglas establecidas
        for fila in range(20):
            for columna in range(20):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    individuo = poblacion[individuo_id - 1]
                    if columna < 19:
                        if cuadricula[fila][columna + 1] == 0:
                            # Mover el individuo según las probabilidades de movimiento
                            movimientos = ['norte', 'sur', 'este', 'oeste', 'diag_ne', 'diag_no', 'diag_se', 'diag_so', 'no_moverse']
                            pesos = individuo['genes'][:9]  # Tomar los primeros 9 valores del vector de genes
                            movimiento = random.choices(movimientos, weights=pesos, k=1)[0]
                            nueva_fila = fila
                            nueva_columna = columna
                            if movimiento == 'norte':
                                nueva_fila -= 1
                            elif movimiento == 'sur':
                                nueva_fila += 1
                            elif movimiento == 'este':
                                nueva_columna += 1
                            elif movimiento == 'oeste':
                                nueva_columna -= 1
                            elif movimiento == 'diag_ne':
                                nueva_fila -= 1
                                nueva_columna += 1
                            elif movimiento == 'diag_no':
                                nueva_fila -= 1
                                nueva_columna -= 1
                            elif movimiento == 'diag_se':
                                nueva_fila += 1
                                nueva_columna += 1
                            elif movimiento == 'diag_so':
                                nueva_fila += 1
                                nueva_columna -= 1

                            # Evitar salir de los límites de la cuadrícula
                            if nueva_fila >= 0 and nueva_fila <= 19 and nueva_columna >= 0 and nueva_columna <= 19:
                                if cuadricula_actual[nueva_fila][nueva_columna] == 0:
                                    cuadricula_actual[nueva_fila][nueva_columna] = individuo_id
                                else:
                                    # La casilla está ocupada, mantener al individuo en su posición actual
                                    cuadricula_actual[fila][columna] = individuo_id
                                    print('Individuo {} se ha quedado en su posición actual'.format(individuo_id))
                            else:
                                # El individuo ha llegado al final de la cuadrícula
                                cuadricula_actual[fila][columna] = individuo_id
                        else:
                            # El individuo ha llegado a la última columna y se queda en su posición
                            cuadricula_actual[fila][columna] = individuo_id
                    else:
                        # El individuo ha llegado al final de la cuadrícula
                        cuadricula_actual[fila][columna] = individuo_id
                        print('Individuo {} ha llegado a la última columna'.format(individuo_id))
                        

        # Actualizar la cuadrícula
        cuadricula = cuadricula_actual

        # Actualizar el gráfico
        ax.clear()
        ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=len(poblacion))
        for fila in range(20):
            for columna in range(20):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
        ax.grid(True, color='black', linewidth=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
        plt.pause(0.1)  # Pausa para actualizar la gráfica

    # Cambiar el color de los individuos que han llegado al final a verde
    for fila in range(20):
        for columna in range(20):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                colores[individuo_id - 1] = '#00FF00'  # Cambiar el color a verde

    # Actualizar el gráfico final sin cerrarlo
    ax.clear()
    ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=len(poblacion))
    for fila in range(20):
        for columna in range(20):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
    ax.grid(True, color='black', linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Columna')
    ax.set_ylabel('Fila')
    plt.show()




def main():
    # Inicializar poblacion
    poblacion = crear_poblacion(20,100)
    print(poblacion)
    grafico = plot_cuadricula(poblacion, 'Población inicial',100)

    #grafico2 = plot_cuadricula_ESPARTANA(poblacion, 'Población final')
    return 0




if __name__ == "__main__":
    main()
