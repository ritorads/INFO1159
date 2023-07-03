import random
import numpy as np
import matplotlib.pyplot as plt
import argparse


def normalizar_vector(vector):
    suma = sum(vector)
    vector_normalizado = [valor / suma for valor in vector]
    return vector_normalizado


def crear_poblacion(num_individuos, contador_movimientos, probabilidad_asesino):
    poblacion = []

    for _ in range(num_individuos):
        cromosoma = creacion_cromosomas(8, contador_movimientos, probabilidad_asesino)
        poblacion.append(cromosoma)

    return poblacion


def creacion_cromosomas(num_genes, contador_movimientos, probabilidad_asesino):
    # Genera las probabilidades aleatorias
    probabilidades = [random.random() for _ in range(num_genes)]

    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)

    # Genera el campo "ID" con la probabilidad para asesinos o normales
    if random.random() < probabilidad_asesino:
        ID = "A"
    else:
        ID = "N"

    # Crea el cromosoma con probabilidades aleatorias, contador de movimientos y posición actual
    cromosoma = {
        "genes": probabilidades,
        "contador_movimientos": contador_movimientos,
        "posicion_actual": (0, 0),
        "ID": ID,  # Agrega el campo "ID" al cromosoma
    }

    return cromosoma


def plot_cuadricula_Mutados(poblacion, num_generaciones, color):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos
    pasos_maximos = poblacion[0]["contador_movimientos"]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xticks(np.arange(tamano_tablero + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(tamano_tablero + 1) - 0.5, minor=True)

    ax.set_xlabel("DIRECION HACIA LA META -->")
    ax.set_ylabel("INICIO DE INDIVIDUOS")
    ax.grid(which="minor", color="black", linestyle="-", linewidth=1)

    plt.xlabel("Columna")
    plt.ylabel("Fila")

    plt.ion()

    cuadricula = np.zeros((tamano_tablero, tamano_tablero))

    for i, individuo in enumerate(poblacion):
        cuadricula[i][0] = i + 1
        individuo["posiciones"] = [(i, 0)]

    img = ax.matshow(cuadricula, cmap=color)
    plt.draw()
    plt.pause(0.1)
    cantidad_finalistas = 0
    cantidad_asesinados = 0
    for paso in range(1, poblacion[0]["contador_movimientos"] + 1):
        ax.set_title(f"GENERACION {num_generaciones + 1}, paso {paso + 1}")
        # print(f"Paso {paso}:")
        for i, individuo in enumerate(poblacion):
            movimientos = [
                "sur",
                "este",
                "oeste",
                "noreste",
                "noroeste",
                "sureste",
                "suroeste",
                "mantener",
            ]
            probabilidades = normalizar_vector(individuo["genes"])
            movimiento = np.random.choice(movimientos, p=probabilidades)

            posicion_actual = individuo["posiciones"][-1]

            nueva_fila, nueva_columna = posicion_actual

            if nueva_columna == 0:
                if movimiento == "oeste":
                    movimiento = "este"
                elif movimiento == "noroeste":
                    movimiento = "noreste"
                elif movimiento == "suroeste":
                    movimiento = "sureste"

            if nueva_columna == tamano_tablero - 1:
                movimiento = "mantener"

            if movimiento == "sur":
                nueva_fila -= 1
                if nueva_fila < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "este":
                nueva_columna += 1
                if nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "oeste":
                nueva_columna -= 1
                if nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "noreste":
                nueva_fila -= 1
                nueva_columna += 1
                if nueva_fila < 0 or nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "noroeste":
                nueva_fila -= 1
                nueva_columna -= 1
                if nueva_fila < 0 or nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "sureste":
                nueva_fila += 1
                nueva_columna += 1
                if nueva_fila >= tamano_tablero or nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "suroeste":
                nueva_fila += 1
                nueva_columna -= 1
                if nueva_fila >= tamano_tablero or nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "mantener":
                nueva_fila, nueva_columna = posicion_actual

            if cuadricula[nueva_fila][nueva_columna] != 0:
                if individuo["ID"] == "N":
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
                elif individuo["ID"] == "A":
                    # Eliminar el individuo de la población
                    print("se elimino un individuo")
                    cantidad_asesinados += 1
                    poblacion = [ind for ind in poblacion if ind != individuo]

            individuo["posiciones"].append((nueva_fila, nueva_columna))

            if nueva_columna != tamano_tablero - 1:
                individuo["contador_movimientos"] -= 1

    cuadricula = np.zeros((tamano_tablero, tamano_tablero))

    for i, individuo in enumerate(poblacion):
        fila, columna = individuo["posiciones"][-1]
        cuadricula[fila][columna] = i + 1

    img.set_data(cuadricula)

    plt.draw()
    plt.pause(1)
    plt.close()

    for individuo in poblacion:
        individuo["posicion_actual"] = individuo["posiciones"][-1]

    for individuo in poblacion:
        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            cantidad_finalistas += 1

    seleccion = seleccion_padres(poblacion, pasos_maximos, tamano_tablero)
    print(f"cantidad de finalistas: {cantidad_finalistas}")

    return seleccion, cantidad_finalistas, cantidad_asesinados


def plot_cuadricula(poblacion, num_generaciones, color):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos
    pasos_maximos = poblacion[0]["contador_movimientos"]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xticks(np.arange(tamano_tablero + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(tamano_tablero + 1) - 0.5, minor=True)

    ax.set_xlabel("DIRECION HACIA LA META -->")
    ax.set_ylabel("INICIO DE INDIVIDUOS")
    ax.grid(which="minor", color="black", linestyle="-", linewidth=1)

    plt.xlabel("Columna")
    plt.ylabel("Fila")

    plt.ion()

    cuadricula = np.zeros((tamano_tablero, tamano_tablero))

    for i, individuo in enumerate(poblacion):
        cuadricula[i][0] = i + 1
        individuo["posiciones"] = [(i, 0)]

    img = ax.matshow(cuadricula, cmap=color)
    plt.draw()
    plt.pause(0.1)
    cantidad_finalistas = 0
    cantidad_asesinados = 0
    for paso in range(1, poblacion[0]["contador_movimientos"] + 1):
        ax.set_title(f"GENERACION {num_generaciones + 1}, paso {paso + 1}")
        # print(f"Paso {paso}:")
        for i, individuo in enumerate(poblacion):
            movimientos = [
                "sur",
                "este",
                "oeste",
                "noreste",
                "noroeste",
                "sureste",
                "suroeste",
                "mantener",
            ]
            probabilidades = normalizar_vector(individuo["genes"])
            movimiento = np.random.choice(movimientos, p=probabilidades)

            posicion_actual = individuo["posiciones"][-1]

            nueva_fila, nueva_columna = posicion_actual

            if nueva_columna == 0:
                if movimiento == "oeste":
                    movimiento = "este"
                elif movimiento == "noroeste":
                    movimiento = "noreste"
                elif movimiento == "suroeste":
                    movimiento = "sureste"

            if nueva_columna == tamano_tablero - 1:
                movimiento = "mantener"

            if movimiento == "sur":
                nueva_fila -= 1
                if nueva_fila < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "este":
                nueva_columna += 1
                if nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "oeste":
                nueva_columna -= 1
                if nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "noreste":
                nueva_fila -= 1
                nueva_columna += 1
                if nueva_fila < 0 or nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "noroeste":
                nueva_fila -= 1
                nueva_columna -= 1
                if nueva_fila < 0 or nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "sureste":
                nueva_fila += 1
                nueva_columna += 1
                if nueva_fila >= tamano_tablero or nueva_columna >= tamano_tablero:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "suroeste":
                nueva_fila += 1
                nueva_columna -= 1
                if nueva_fila >= tamano_tablero or nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "mantener":
                nueva_fila, nueva_columna = posicion_actual

            if cuadricula[nueva_fila][nueva_columna] != 0:
                if individuo["ID"] == "N":
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
                elif individuo["ID"] == "A":
                    # Eliminar el individuo de la población
                    print("se elimino un individuo")
                    cantidad_asesinados += 1
                    poblacion = [ind for ind in poblacion if ind != individuo]

            individuo["posiciones"].append((nueva_fila, nueva_columna))

            if nueva_columna != tamano_tablero - 1:
                individuo["contador_movimientos"] -= 1

    cuadricula = np.zeros((tamano_tablero, tamano_tablero))

    for i, individuo in enumerate(poblacion):
        fila, columna = individuo["posiciones"][-1]
        cuadricula[fila][columna] = i + 1

    img.set_data(cuadricula)

    plt.draw()
    plt.pause(1)
    plt.close()

    for individuo in poblacion:
        individuo["posicion_actual"] = individuo["posiciones"][-1]

    for individuo in poblacion:
        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            cantidad_finalistas += 1

    seleccion = seleccion_padres(poblacion, pasos_maximos, tamano_tablero)
    print(f"cantidad de finalistas: {cantidad_finalistas}")
    return seleccion, cantidad_finalistas, cantidad_asesinados


def seleccion_padres(poblacion, pasos_maximos, tamano_tablero):
    gen_prueba = [
        {"contador_movimientos": pasos_maximos + 1, "posicion_actual": (0, 0), "id": 0}
    ]
    Mejores_individuos = [gen_prueba[0], gen_prueba[0]]

    print("INDIVIDUOS QUE LLEGARON AL FINAL")
    print("================================")
    for i, individuo in enumerate(poblacion):
        posicion_1 = individuo["posiciones"]
        posiciones_sin_repetir = len(list(set(posicion_1)))
        print(f"individuo {i}, posiciones {posiciones_sin_repetir}")
        # print(f"posiciones :{posiciones_sin_repetir}")
        # print(f"cantidad de pasos : {posiciones_sin_repetir}")
        individuo["contador_movimientos"] = posiciones_sin_repetir
        individuo["id"] = i + 1

        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            if posiciones_sin_repetir < Mejores_individuos[0]["contador_movimientos"]:
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

    if (
        Mejores_individuos[0]["contador_movimientos"] == pasos_maximos + 1
        or Mejores_individuos[1]["contador_movimientos"] == pasos_maximos + 1
    ):
        return []  # Return an empty list instead of the string

    elif (
        Mejores_individuos[1]["contador_movimientos"] != pasos_maximos + 1
        and Mejores_individuos[0]["contador_movimientos"] != pasos_maximos + 1
    ):
        print(
            f"MEJORES INDIVIDUOS \n 1er lugar : {Mejores_individuos[0]['id']}, posicion{Mejores_individuos[0]['posicion_actual']}, contador pasos {Mejores_individuos[0]['contador_movimientos']} \
                \n 2do lugar : {Mejores_individuos[1]['id']}, posicion{Mejores_individuos[1]['posicion_actual']}, contador pasos {Mejores_individuos[1]['contador_movimientos']}"
        )
        return Mejores_individuos


def funcionamiento_principal(
    Cantidad_generaciones,
    Cantidad_Individuos,
    cantidad_movimientos,
    probabilidad_asesino,
    Probabilidad_mutacion,
):  ## def Obtener2padres():
    cantidades = []
    asesinados = []
    Generacion_Actual = 0
    Hay_mutacion = 0
    while Generacion_Actual < Cantidad_generaciones:
        while Hay_mutacion == 0:
            poblacion = crear_poblacion(
                Cantidad_Individuos, cantidad_movimientos, probabilidad_asesino
            )  # Ejemplo con 10 individuos y 10 movimientos
            resultado_A = plot_cuadricula(poblacion, Generacion_Actual, color="Blues")
            cantidades.append(resultado_A[1])
            asesinados.append(resultado_A[2])
            Generacion_Actual += 1

            if resultado_A[0] != []:
                poblacion = cruzar_cromosomas(
                    resultado_A[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula_Mutados(
                    poblacion, Generacion_Actual, color="Reds"
                )
                cantidades.append(resultado[1])
                asesinados.append(resultado[2])
                resultado_anterior = resultado_A
                resultado_temp = resultado
                Generacion_Actual += 1
                Hay_mutacion = 1

        while Hay_mutacion == 1 and Generacion_Actual < Cantidad_generaciones:
            print(Cantidad_generaciones)
            print(Generacion_Actual)
            if resultado_temp[0] != []:
                print("mas de one")
                poblacion = cruzar_cromosomas(
                    resultado_temp[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula_Mutados(
                    poblacion, Generacion_Actual, color="Reds"
                )
                cantidades.append(resultado[1])
                asesinados.append(resultado[2])
                resultado_anterior = resultado_temp
                resultado_temp = resultado
                Generacion_Actual += 1
            else:
                print("one o ninguno")
                poblacion = cruzar_cromosomas(
                    resultado_anterior[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula_Mutados(
                    poblacion, Generacion_Actual, color="Blues"
                )
                cantidades.append(resultado[1])
                asesinados.append(resultado[2])
                resultado_anterior = resultado_anterior
                resultado_temp = resultado
                Generacion_Actual += 1
    if Cantidad_generaciones >= Generacion_Actual:
        print("limite sobrepasado")

    generaciones = list(range(Cantidad_generaciones))
    porcentajes = [finalistas / Cantidad_Individuos * 100 for finalistas in cantidades]
    print(cantidades)
    print(porcentajes)
    print(asesinados)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))

    # Gráfico de la cantidad de individuos que llegaron
    ax1.plot(generaciones, cantidades)
    ax1.set_xlabel("Generación")
    ax1.set_ylabel("Cantidad de finalistas")
    ax1.set_title("Evolución de la cantidad de finalistas por generación")

    # Agregar el porcentaje sobre cada punto del gráfico de cantidad
    for gen, cant in zip(generaciones, cantidades):
        ax1.text(gen, cant, f"{cant:.2f}", ha="center", va="bottom")

    # Gráfico del porcentaje de individuos que llegaron
    ax2.plot(generaciones, porcentajes)
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Porcentaje de finalistas")
    ax2.set_title("Evolución del porcentaje de finalistas por generación")

    # Agregar el porcentaje sobre cada punto del gráfico de porcentaje
    for gen, pct in zip(generaciones, porcentajes):
        ax2.text(gen, pct, f"{pct:.2f}%", ha="center", va="bottom")

    # Gráfico de la cantidad de individuos que murieron
    ax3.plot(generaciones, asesinados)
    ax3.set_xlabel("Generación")
    ax3.set_ylabel("Cantidad de individuos muertos")
    ax3.set_title("Evolución de la cantidad de individuos muertos por generación")

    # Agregar el número sobre cada punto del gráfico de cantidad de muertos
    for gen, muertos in zip(generaciones, asesinados):
        ax3.text(gen, muertos, str(muertos), ha="center", va="bottom")

    plt.tight_layout()  # Ajustar el espacio entre los subgráficos
    plt.savefig("grafico.png")
    plt.close()

    # Abrir el archivo de imagen para ver los gráficos
    from PIL import Image

    Image.open("grafico.png").show()


def cruzar_cromosomas(
    Mejores_individuos, cantidad_poblacion, probabilidad_asesino, probabilidad_mutacion
):
    print("Cruce de cromosomas")

    # Seleccionar los dos mejores individuos
    individuo_1 = Mejores_individuos[0]
    individuo_2 = Mejores_individuos[1]

    # print(f"individuo 1 : {Mejores_individuos}")

    # Seleccionar los cromosomas de los dos mejores individuos
    cromosoma_1 = individuo_1["genes"]
    cromosoma_2 = individuo_2["genes"]

    print(cromosoma_1)
    print(cromosoma_2)
    # posiciones
    posicion_1 = individuo_1["posiciones"]

    posiciones_sin_repetir = list(set(posicion_1))

    # print(f"posiciones :{posiciones_sin_repetir}")
    # print(f"cantidad de pasos : {len(posiciones_sin_repetir)}")
    # Crear la nueva población
    nueva_poblacion = []
    print(probabilidad_mutacion)

    for i in range(cantidad_poblacion):
        punto_cruce = random.randint(0, len(cromosoma_1) - 1)
        gen_hijo = cromosoma_1[:punto_cruce] + cromosoma_2[punto_cruce:]
        gen_mutado = mutar_cromosomas(gen_hijo, probabilidad_mutacion)
        gen_mutado_normalizado = normalizar_vector(gen_mutado)
        if random.random() < probabilidad_asesino:
            ID = "A"
        else:
            ID = "N"
        cromosomas_hijos = {
            "genes": gen_mutado_normalizado,
            "contador_movimientos": 40,
            "posicion_actual": [0],
            "ID": ID,
        }
        nueva_poblacion.append(cromosomas_hijos)

    # for i, individuos in enumerate(nueva_poblacion):
    #    print(f"Individuo {i} : {individuos['genes']}")

    return nueva_poblacion


def mutar_cromosomas(cromosoma, probabilidad_mutacion):
    # Seleccionar el gen a mutar
    gen_a_mutar = random.randint(0, len(cromosoma) - 1)

    # Seleccionar el nuevo valor del gen < 1
    nuevo_valor = random.uniform(0, probabilidad_mutacion)

    # Mutar el gen
    cromosoma[gen_a_mutar] = nuevo_valor

    return cromosoma


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmo genético")
    parser.add_argument(
        "--generaciones", type=int, help="Cantidad de generaciones maximas"
    )
    parser.add_argument("--individuos", type=int, help="Cantidad Individuos")
    parser.add_argument("--movimientos", type=int, help="Cantidad de movimientos")
    parser.add_argument("--probabilidad", type=float, help="Probabilidad de asesino")
    parser.add_argument("--mutacion", type=float, help="Probabilidad de mutacion")

    args = parser.parse_args()
    print(args.probabilidad)

    funcionamiento_principal(
        args.generaciones,
        args.individuos,
        args.movimientos,
        args.probabilidad,
        args.mutacion,
    )

    # funcionamiento_principal(40, 20, 70)

    # python .\Testeos_rito.py --generaciones 20 --individuos 20 --movimientos 50
    # Cantidad_generaciones, Cantidad_Individuos, cantidad_movimientos
