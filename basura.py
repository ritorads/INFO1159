import random
import numpy as np
import matplotlib.pyplot as plt
import argparse
from PIL import Image

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


def plot_cuadricula(opciones, iteraciones, poblacion, num_generaciones, color,Probabilidad_asesinar,filas,columnas):
    num_individuos = len(poblacion)
    tamano_tablero = num_individuos
    cantidad_asesinos = 0
    pasos_maximos = poblacion[0]["contador_movimientos"]

    if opciones == "Si":
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)

        ax.set_xticks(np.arange(columnas + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(filas + 1) - 0.5, minor=True)
        # Ajustar el tamaño de las celdas
        ax.set_xlim([-0.5, columnas - 0.5])
        ax.set_ylim([-0.5, filas - 0.5])
        ax.set_xlabel("DIRECION HACIA LA META -->")
        ax.set_ylabel("INICIO DE INDIVIDUOS")
        ax.set_aspect('equal')
        ax.grid(which="minor", color="black", linestyle="-", linewidth=1)


        plt.ion()

    cuadricula = np.zeros((filas, columnas))
    ##################################################
    for i, individuo in enumerate(poblacion):
        cuadricula[i][0] = i + 1
        individuo["posiciones"] = [(i, 0)]

    #Opcion para ver la cuadricula    
    if opciones == "Si":
        img = ax.matshow(cuadricula, cmap=color)
        plt.draw()
        plt.pause(0.1)
    cantidad_finalistas = 0
    cantidad_asesinados = 0
    for paso in range(1, poblacion[0]["contador_movimientos"] + 1):
        if opciones == "Si":
            ax.set_title(f"GENERACION {num_generaciones}, paso {paso + 1}")
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
            #Condicionales para que no se salga de la cuadricula
            if nueva_columna == 0:
                if movimiento == "oeste":
                    movimiento = "este"
                elif movimiento == "noroeste":
                    movimiento = "noreste"
                elif movimiento == "suroeste":
                    movimiento = "sureste"

            if nueva_columna == columnas - 1:
                movimiento = "mantener"

            if movimiento == "sur":
                nueva_fila -= 1
                if nueva_fila < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "este":
                nueva_columna += 1
                if nueva_columna >= columnas:
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
                if nueva_fila < 0 or nueva_columna >= columnas:
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
                if nueva_fila >= filas or nueva_columna >= columnas:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "suroeste":
                nueva_fila += 1
                nueva_columna -= 1
                if nueva_fila >= filas or nueva_columna < 0:
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            elif movimiento == "mantener":
                nueva_fila, nueva_columna = posicion_actual
            ################## CONDICIONAL DEL NORMAL ##################
            if cuadricula[nueva_fila][nueva_columna] != 0:
                if individuo["ID"] == "N":
                    movimiento = "mantener"
                    nueva_fila, nueva_columna = posicion_actual
            ################## CONDICIONAL DEL ASESINO ##################        
                elif individuo["ID"] == "A":
                    # Eliminar el individuo de la población
                    if random.random() < Probabilidad_asesinar:
                        cantidad_asesinados += 1
                        cuadricula[nueva_fila][nueva_columna] = 0

            individuo["posiciones"].append((nueva_fila, nueva_columna))

            if nueva_columna != columnas - 1:
                individuo["contador_movimientos"] -= 1
    #if que imprime la matriz de la poblacion         
    if opciones == "Si":
        cuadricula = np.zeros((filas, columnas))

        for i, individuo in enumerate(poblacion):
            fila, columna = individuo["posiciones"][-1]
            cuadricula[fila][columna] = i + 1

        img.set_data(cuadricula)

        plt.draw()
        plt.pause(1)
        plt.close()
    #for que actualiza la posicion actual de los individuos
    for individuo in poblacion:
        individuo["posicion_actual"] = individuo["posiciones"][-1]
    #for que cuenta la cantidad de finalistas
    for individuo in poblacion:
        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            cantidad_finalistas += 1
    #for para contar cuantos asesinos habia
    for individuo in poblacion:
        if individuo["ID"] == "A":
            cantidad_asesinos += 1
                    
    seleccion = seleccion_padres(poblacion, pasos_maximos, tamano_tablero)
    print(f"cantidad de finalistas: {cantidad_finalistas}")
    return seleccion, cantidad_finalistas, cantidad_asesinados, cantidad_asesinos


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
    iteraciones,
    opciones,
    Probabilidad_Asesinar,
    filas,
    columnas,
):  ## def Obtener2padres():
    cantidades = []
    asesinados = []
    cantidad_asesinos = []
    Hay_mutacion = 0
    opciones_temp = "No"
    Total_Individuos = Cantidad_Individuos
    Generacion_Actual=0
    Color_Blue= "Blues"
    Color_Red= "Reds"
    while Generacion_Actual < Cantidad_generaciones:
        while Hay_mutacion == 0:
            if Generacion_Actual % iteraciones == 0 and opciones == "Si":
                print("generacion actual", Generacion_Actual)
                opciones_temp = "Si"
            elif Generacion_Actual % iteraciones != 0 and opciones == "Si":
                opciones_temp = "No"

            poblacion = crear_poblacion(
                Cantidad_Individuos, cantidad_movimientos, probabilidad_asesino
            )  # Ejemplo con 10 individuos y 10 movimientos
            resultado_A = plot_cuadricula(
                opciones_temp, iteraciones, poblacion, Generacion_Actual, Color_Blue,Probabilidad_Asesinar,filas,columnas
            )
            cantidades.append(resultado_A[1])
            asesinados.append(resultado_A[2])
            cantidad_asesinos.append(resultado_A[3])
            Generacion_Actual += 1
            ##############################################
            if Generacion_Actual == Cantidad_generaciones:# <-- CONDICIONAL PARA SALIR DEL CICLO SI NO LLEGA NUNCA NADIE EN LAS GENERACIONES
                break                                     
            ##############################################
            if resultado_A[0] != []:
                poblacion = cruzar_cromosomas(
                    resultado_A[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula(
                    opciones_temp,
                    iteraciones,
                    poblacion,
                    Generacion_Actual,
                    Color_Red,
                    Probabilidad_Asesinar,
                    filas,
                    columnas
                )
                cantidades.append(resultado[1])
                asesinados.append(resultado[2])
                cantidad_asesinos.append(resultado_A[3])
                resultado_anterior = resultado_A
                resultado_temp = resultado
                Generacion_Actual += 1 
                Hay_mutacion = 1

        while Hay_mutacion == 1 and Generacion_Actual < Cantidad_generaciones:
            if Generacion_Actual % iteraciones == 0 and opciones == "Si":
                print("generacion actual", Generacion_Actual)
                opciones_temp = "Si"
            elif Generacion_Actual % iteraciones != 0 and opciones == "Si":
                opciones_temp = "No"

            if resultado_temp[0] != []:
                print("mas de one")
                poblacion = cruzar_cromosomas(
                    resultado_temp[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula(
                    opciones_temp,
                    iteraciones,
                    poblacion,
                    Generacion_Actual,
                    Color_Red,
                    Probabilidad_Asesinar,
                    filas,
                    columnas
                )
                cantidades.append(resultado[1]) # <-- SE GUARDA LA CANTIDAD DE INDIVIDUOS QUE LLEGARON A LA META
                asesinados.append(resultado[2]) # <-- SE GUARDA LA CANTIDAD DE INDIVIDUOS QUE FUERON ASESINADOS
                cantidad_asesinos.append(resultado_A[3])
                resultado_anterior = resultado_temp # <-- SE GUARDA EL RESULTADO ANTERIOR PARA QUE SE PUEDA CRUZAR CON EL SIGUIENTE
                resultado_temp = resultado # <-- SE GUARDA EL RESULTADO ACTUAL PARA QUE SE PUEDA CRUZAR CON EL SIGUIENTE

                Generacion_Actual += 1

            else:
                print("one o ninguno")
                poblacion = cruzar_cromosomas(
                    resultado_anterior[0],
                    Cantidad_Individuos,
                    probabilidad_asesino,
                    Probabilidad_mutacion,
                )
                resultado = plot_cuadricula(
                    opciones_temp,
                    iteraciones,
                    poblacion,
                    Generacion_Actual,
                    Color_Blue,
                    Probabilidad_Asesinar,
                    filas,
                    columnas
                )
                cantidades.append(resultado[1])
                asesinados.append(resultado[2])
                resultado_anterior = resultado_anterior
                resultado_temp = resultado

    if Cantidad_generaciones >= Generacion_Actual:
        print("limite sobrepasado")

    generaciones = list(range(Cantidad_generaciones))
    porcentajes = [finalistas / Cantidad_Individuos * 100 for finalistas in cantidades]
    sobrevivientes = [Total_Individuos-asesinados for asesinados in cantidad_asesinos]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

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
    ax3.plot(generaciones, cantidad_asesinos)
    ax3.set_xlabel("Generación")
    ax3.set_ylabel("Cantidad de individuos muertos")
    ax3.set_title("Evolución de la cantidad de individuos muertos por generación")

    # Agregar el número sobre cada punto del gráfico de cantidad de muertos
    for gen, muertos in zip(generaciones, cantidad_asesinos):
        ax3.text(gen, muertos, str(muertos), ha="center", va="bottom")

    # Gráfico de la cantidad de sobrevivientes en relación a los asesinos
    ax4.plot(generaciones, sobrevivientes)
    ax4.set_xlabel("Generación")
    ax4.set_ylabel("Cantidad de sobrevivientes")
    ax4.set_title("Evolución de la cantidad de sobrevivientes por generación")

    # Agregar la cantidad sobre cada punto del gráfico de sobrevivientes
    for gen, sobrevivientes_gen in zip(generaciones, sobrevivientes):
        ax4.text(gen, sobrevivientes_gen, str(sobrevivientes_gen), ha="center", va="bottom")

    plt.tight_layout()  # Ajustar el espacio entre los subgráficos
    plt.savefig("grafico.png")
    plt.close()

# Abrir el archivo de imagen para ver los gráficos
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


def No_Negatividad(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} no puede ser negativo")
    return ivalue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmo genético")
    parser.add_argument(
        "--generaciones",
        type=No_Negatividad,
        help="Cantidad de generaciones máximas",
        required=True,
    )
    parser.add_argument(
        "--individuos",
        type=No_Negatividad,
        help="Cantidad de individuos",
        required=True,
    )
    parser.add_argument(
        "--movimientos",
        type=No_Negatividad,
        help="Cantidad de movimientos",
        required=True,
    )
    parser.add_argument(
        "--probabilidad", type=float, help="Probabilidad de asesino", required=True
    )
    parser.add_argument(
        "--mutacion", type=float, help="Probabilidad de mutación", required=True
    )
    parser.add_argument(
        "--iteraciones",
        type=No_Negatividad,
        help="Cantidad de iteraciones",
        required=True,
    )
    parser.add_argument(
        "--ProbabilidadAsesinar",
        type=float,
        help="Probabilidad de Asesinar un individuo",
        required=True,
    )
    parser.add_argument(
        "--Filas",
        type=No_Negatividad,
        help="Cantidad de Filas",
        required=True,
    )
    parser.add_argument(
        "--Columnas",
        type=No_Negatividad,
        help="Cantidad de Columnas",
        required=True,
    )
    parser.add_argument(
        "--opciones",
        type=str,
        help="Opciones 'Si' o 'No'",
        choices=["Si", "No"],
        required=True,
    )

    args = parser.parse_args()

    funcionamiento_principal(
        args.generaciones,
        args.individuos,
        args.movimientos,
        args.probabilidad,
        args.mutacion,
        args.iteraciones,
        args.opciones,
        args.ProbabilidadAsesinar,
        args.Filas,
        args.Columnas,
    )

    # funcionamiento_principal(40, 20, 70)

    # python .\Testeos_rito.py --generaciones 20 --individuos 20 --movimientos 50
    # Cantidad_generaciones, Cantidad_Individuos, cantidad_movimientos
