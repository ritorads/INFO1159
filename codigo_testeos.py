import random
import matplotlib.pyplot as plt


def normalizar_vector(vector):
    suma = sum(vector)
    vector_normalizado = [valor / suma for valor in vector]
    return vector_normalizado


def crear_poblacion(num_individuos, contador_movimientos):
    poblacion = []

    for _ in range(num_individuos):
        cromosoma = creacion_cromosomas(9, contador_movimientos)
        poblacion.append(cromosoma)

    return poblacion


def creacion_cromosomas(num_genes, contador_movimientos):
    # Genera las probabilidades aleatorias
    probabilidades = [random.random() for _ in range(num_genes)]

    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)

    # Crea el cromosoma con probabilidades aleatorias, contador de movimientos y posición actual
    cromosoma = {
        'genes': probabilidades,
        'contador_movimientos': contador_movimientos,
        'posicion_actual': (0, 0)  # Inicialmente todos los individuos están en la posición (0, 0)
    }

    return cromosoma

def plot_cuadricula(poblacion):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Cuadrícula")

    cuadricula = [[0] * tamano_tablero for _ in range(tamano_tablero)]
    colores = ['#0330FF'] * num_individuos

    for i, individuo in enumerate(poblacion):
        fila = i
        cuadricula[fila][0] = i + 1

    pasos_maximos = poblacion[0]['contador_movimientos']  # Utilizar contador_movimientos del primer cromosoma
    for paso in range(pasos_maximos):
        cuadricula_actual = [[0] * tamano_tablero for _ in range(tamano_tablero)]

        for fila in range(tamano_tablero):
            for columna in range(tamano_tablero):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    individuo = poblacion[individuo_id - 1]
                    if columna < tamano_tablero - 1:
                        if cuadricula[fila][columna + 1] == 0:
                            movimientos = ['norte', 'sur', 'este', 'oeste', 'diag_ne', 'diag_no', 'diag_se', 'diag_so',
                                           'no_moverse']
                            pesos = individuo['genes'][:9]
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

                            if nueva_fila >= 0 and nueva_fila < tamano_tablero and nueva_columna >= 0 and nueva_columna < tamano_tablero:
                                if cuadricula_actual[nueva_fila][nueva_columna] == 0:
                                    cuadricula_actual[nueva_fila][nueva_columna] = individuo_id
                                    individuo['posicion_actual'] = (nueva_fila, nueva_columna)  # Update posicion_actual
                                    if nueva_columna == tamano_tablero - 1:
                                        print('Individuo {} ha llegado a la última columna y ha sido detectado'.format(individuo_id))
                                        print('contador_movimientos: {}'.format(individuo['contador_movimientos']))
                                    individuo['contador_movimientos'] -= 1  # Decrement contador_movimientos
                                    if individuo['contador_movimientos'] == 0:
                                        cuadricula_actual[fila][columna] = 0  # Individuo se queda en su posición actual
                                else:
                                    cuadricula_actual[fila][columna] = individuo_id
                                    print('Individuo {} se ha quedado en su posición actual'.format(individuo_id))
                            else:
                                cuadricula_actual[fila][columna] = individuo_id
                        else:
                            cuadricula_actual[fila][columna] = individuo_id
                    else:
                        cuadricula_actual[fila][columna] = individuo_id
                        # print('Individuo {} ha llegado a la última columna'.format(individuo_id))

        cuadricula = cuadricula_actual

        ax.clear()
        ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=num_individuos)
        for fila in range(tamano_tablero):
            for columna in range(tamano_tablero):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
        ax.grid(True, color='black', linewidth=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
        plt.pause(0.1)

    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                colores[individuo_id - 1] = '#00FF00'

    ax.clear()
    ax.imshow(cuadricula, cmap='Blues', vmin=0, vmax=num_individuos)
    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                ax.text(columna, fila, individuo_id, color=colores[individuo_id - 1], ha='center', va='center')
    ax.grid(True, color='black', linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Columna')
    ax.set_ylabel('Fila')
    plt.show()
    print('Fin del algoritmo genético')
    print('INDIVIDUOS QUE LLEGARON AL FINAL')
    print('================================')
    for i, individuo in enumerate(poblacion):
        if individuo['posicion_actual'][1] == tamano_tablero - 1:
         print('Individuo {}: contador_movimientos: {}'.format(i + 1, individuo['contador_movimientos']))
         print('Individuo {}: genes: {}'.format(i + 1, individuo['genes']))
         print('Individuo {}: posicion_actual: {}'.format(i + 1, individuo['posicion_actual']))
    print('================================')
# Crear población inicial de 5 individuos con 30 movimientos
pobla = crear_poblacion(20, 100)

# Ejecutar algoritmo genético
plot_cuadricula(pobla)
