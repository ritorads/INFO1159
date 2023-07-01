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
        "genes": probabilidades,
        "contador_movimientos": contador_movimientos,
        "posicion_actual": (
            0,
            0,
        ),  # Inicialmente todos los individuos están en la posición (0, 0)
    }

    return cromosoma


def plot_cuadricula(poblacion, num_generaciones):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Cuadrícula")

    cuadricula = [[0] * tamano_tablero for _ in range(tamano_tablero)]
    colores = ["#0330FF"] * num_individuos

    for i, individuo in enumerate(poblacion):
        fila = i
        cuadricula[fila][0] = i + 1

    pasos_maximos = poblacion[0][
        "contador_movimientos"
    ]  # Utilizar contador_movimientos del primer cromosoma
    for paso in range(pasos_maximos):
        cuadricula_actual = [[0] * tamano_tablero for _ in range(tamano_tablero)]

        for fila in range(tamano_tablero):
            for columna in range(tamano_tablero):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    individuo = poblacion[individuo_id - 1]
                    if columna < tamano_tablero - 1:
                        if cuadricula[fila][columna + 1] == 0:
                            movimientos = [
                                "norte",
                                "sur",
                                "este",
                                "oeste",
                                "diag_ne",
                                "diag_no",
                                "diag_se",
                                "diag_so",
                                "no_moverse",
                            ]
                            pesos = individuo["genes"][:9]
                            movimiento = random.choices(
                                movimientos, weights=pesos, k=1
                            )[0]
                            nueva_fila = fila
                            nueva_columna = columna
                            if movimiento == "norte":
                                nueva_fila -= 1
                            elif movimiento == "sur":
                                nueva_fila += 1
                            elif movimiento == "este":
                                nueva_columna += 1
                            elif movimiento == "oeste":
                                nueva_columna -= 1
                            elif movimiento == "diag_ne":
                                nueva_fila -= 1
                                nueva_columna += 1
                            elif movimiento == "diag_no":
                                nueva_fila -= 1
                                nueva_columna -= 1
                            elif movimiento == "diag_se":
                                nueva_fila += 1
                                nueva_columna += 1
                            elif movimiento == "diag_so":
                                nueva_fila += 1
                                nueva_columna -= 1

                            if (
                                nueva_fila >= 0
                                and nueva_fila < tamano_tablero
                                and nueva_columna >= 0
                                and nueva_columna < tamano_tablero
                            ):
                                if cuadricula_actual[nueva_fila][nueva_columna] == 0:
                                    cuadricula_actual[nueva_fila][
                                        nueva_columna
                                    ] = individuo_id
                                    individuo["posicion_actual"] = (
                                        nueva_fila,
                                        nueva_columna,
                                    )  # Update posicion_actual
                                    if nueva_columna == tamano_tablero - 1:
                                        """print(
                                            "Individuo {} ha llegado a la última columna y ha sido detectado".format(
                                                individuo_id
                                            )
                                        )
                                        print(
                                            "contador_movimientos: {}".format(
                                                individuo["contador_movimientos"]
                                            )
                                        )
                                        """
                                    individuo[
                                        "contador_movimientos"
                                    ] -= 1  # Decrement contador_movimientos
                                    if individuo["contador_movimientos"] == 0:
                                        cuadricula_actual[fila][
                                            columna
                                        ] = 0  # Individuo se queda en su posición actual
                                else:
                                    cuadricula_actual[fila][columna] = individuo_id
                                    # print(
                                    #   "Individuo {} se ha quedado en su posición actual".format(
                                    #      individuo_id
                                    # )
                                    # )
                            else:
                                cuadricula_actual[fila][columna] = individuo_id
                        else:
                            cuadricula_actual[fila][columna] = individuo_id
                    else:
                        cuadricula_actual[fila][columna] = individuo_id
                        # print('Individuo {} ha llegado a la última columna'.format(individuo_id))

        cuadricula = cuadricula_actual

        ax.clear()
        ax.imshow(cuadricula, cmap="Blues", vmin=0, vmax=num_individuos)
        for fila in range(tamano_tablero):
            for columna in range(tamano_tablero):
                individuo_id = cuadricula[fila][columna]
                if individuo_id != 0:
                    ax.text(
                        columna,
                        fila,
                        individuo_id,
                        color=colores[individuo_id - 1],
                        ha="center",
                        va="center",
                    )
        ax.grid(True, color="black", linewidth=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("GENERACION {}, PASO {}".format(num_generaciones, paso + 1))
        ax.set_xlabel("DIRECION HACIA LA META -->")
        ax.set_ylabel("INICIO DE INDIVIDUOS")
        plt.pause(0.001)

    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                colores[individuo_id - 1] = "#00FF00"

    ax.clear()

    ax.imshow(cuadricula, cmap="Blues", vmin=0, vmax=num_individuos)
    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            individuo_id = cuadricula[fila][columna]
            if individuo_id != 0:
                ax.text(
                    columna,
                    fila,
                    individuo_id,
                    color=colores[individuo_id - 1],
                    ha="center",
                    va="center",
                )
    ax.grid(True, color="black", linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Columna")
    ax.set_ylabel("Fila")
    print("Fin del algoritmo genético")

    Seleccion = seleccion_padres(poblacion, pasos_maximos, tamano_tablero)

    plt.close()  # Cerrar automáticamente la ventana de la gráfica

    return Seleccion


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
    return 0


##############################################################################################################
def funcionamiento_principal(
    Cantidad_generaciones, Cantidad_Individuos, Cantidad_Pasos
):
    Generacion_Actual = 0
    poblacion_actual = []
    while Generacion_Actual < Cantidad_generaciones:
        while True:
            if len(poblacion_actual) == 0:
                print("-----------------------------------------------------")
                poblacion = crear_poblacion(
                    Cantidad_Individuos, Cantidad_Pasos
                )  # Ejemplo con 10 individuos y 10 movimientos
                resultado = plot_cuadricula(poblacion, Generacion_Actual)
                Generacion_Actual += 1
                if (
                    resultado != "Ningún individuo llegó al final"
                    or Generacion_Actual == Cantidad_generaciones
                ):
                    print("fue esto")
                    break
            else:
                resultado = cruzar_cromosomas(
                    poblacion_actual
                )  # Actualizar la población actual
                poblacion_actual = resultado
                resultado = plot_cuadricula(poblacion_actual, Generacion_Actual)
                Generacion_Actual += 1
                if (
                    resultado != "Ningún individuo llegó al final"
                    or Generacion_Actual == Cantidad_generaciones
                ):
                    print("fue esto")
                    break

        Generacion_Actual += 1
        print("==================================")
        print("Generación actual: ", Generacion_Actual)
        print("==================================")


def cruzar_cromosomas(Mejores_individuos):
    print("Cruce de cromosomas")
    print("===================")

    # Seleccionar los dos mejores individuos
    individuo_1 = Mejores_individuos[0]
    individuo_2 = Mejores_individuos[1]

    # Seleccionar los cromosomas de los dos mejores individuos
    cromosoma_1 = individuo_1["genes"]
    cromosoma_2 = individuo_2["genes"]

    # Seleccionar el punto de cruce
    punto_cruce = random.randint(0, len(cromosoma_1) - 1)

    # Crear la nueva población
    nueva_poblacion = []
    for i in range(19):
        gen_hijo = cromosoma_1[:punto_cruce] + cromosoma_2[punto_cruce:]
        gen_mutado = mutar_cromosomas(gen_hijo)
        gen_mutado_normalizado = normalizar_vector(gen_mutado)

        cromosomas_hijos = {
            "genes": gen_mutado_normalizado,
            "contador_movimientos": 50,
            "posicion_actual": (0, 0),
        }
        nueva_poblacion.append(cromosomas_hijos)

    for i, individuos in enumerate(nueva_poblacion):
        print(f"Individuo {i} : {individuos['genes']}")

    return nueva_poblacion


def mutar_cromosomas(cromosoma):
    # Seleccionar el gen a mutar
    gen_a_mutar = random.randint(0, len(cromosoma) - 1)

    # Seleccionar el nuevo valor del gen < 1
    nuevo_valor = random.random()

    # Mutar el gen
    cromosoma[gen_a_mutar] = nuevo_valor

    return cromosoma


PRUEBA = funcionamiento_principal(
    40, 20, 50
)  # Cantidad de generaciones, cantidad de individuos, cantidad de pasos
