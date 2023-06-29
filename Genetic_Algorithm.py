import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Individual:
    def __init__(self, x, y, probabilities):
        self.x = x
        self.y = y
        self.probabilities = probabilities

    def move(self):
        direction = random.choices(
            [
                "north",
                "south",
                "east",
                "west",
                "northeast",
                "northwest",
                "southeast",
                "southwest",
                "stay",
            ],
            weights=self.probabilities,
        )[0]

        if direction == "north":
            self.y = min(self.y + 1, 19)
        elif direction == "south":
            self.y = max(self.y - 1, 0)
        elif direction == "east":
            self.x = min(self.x + 1, 19)
        elif direction == "west":
            self.x = max(self.x - 1, 0)
        elif direction == "northeast":
            self.x = min(self.x + 1, 19)
            self.y = min(self.y + 1, 19)
        elif direction == "northwest":
            self.x = max(self.x - 1, 0)
            self.y = min(self.y + 1, 19)
        elif direction == "southeast":
            self.x = min(self.x + 1, 19)
            self.y = max(self.y - 1, 0)
        elif direction == "southwest":
            self.x = max(self.x - 1, 0)
            self.y = max(self.y - 1, 0)


class GeneticAlgorithm:
    def __init__(self, population_size, grid_size, movement_limit, goal_x):
        self.population_size = population_size
        self.grid_size = grid_size
        self.movement_limit = movement_limit
        self.goal_x = goal_x
        self.population = []
        self.generation = 0

    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            x = 0
            y = random.randint(0, self.grid_size - 1)
            probabilities = self.generate_normalized_probabilities()
            individual = Individual(x, y, probabilities)
            self.population.append(individual)

    def generate_normalized_probabilities(self):
        probabilities = [random.random() for _ in range(9)]
        normalization_factor = sum(probabilities)
        probabilities = [p / normalization_factor for p in probabilities]
        return probabilities

    def simulate_generation(self):
        new_population = []
        for individual in self.population:
            for _ in range(self.movement_limit):
                individual.move()

                if individual.x >= self.goal_x:
                    break

            new_population.append(individual)

        self.population = new_population
        self.generation += 1

    def update_plot(self, frame):
        plt.cla()
        plt.xlim(0, self.grid_size - 1)
        plt.ylim(0, self.grid_size - 1)
        plt.title(f"Generation {self.generation}")

        for individual in self.population:
            plt.scatter(individual.x, individual.y, color="b")

        self.simulate_generation()

    def run(self):
        self.initialize_population()

        fig = plt.figure()
        ani = animation.FuncAnimation(fig, self.update_plot, interval=1000, blit=False)
        plt.show()


# Parámetros del algoritmo
population_size = 20
grid_size = 20
movement_limit = 10
goal_x = grid_size - 1

# Crear instancia del algoritmo genético
genetic_algorithm = GeneticAlgorithm(population_size, grid_size, movement_limit, goal_x)

# Ejecutar el algoritmo
genetic_algorithm.run()
import random
import matplotlib.pyplot as plt


def obtener_fitness(cromosoma):
    # Funcion de fitness
    return 0


def normalizar_vector(vector):
    suma = sum(vector)
    vector_normalizado = [valor / suma for valor in vector]
    return vector_normalizado


def creacion_cromosomas_perfectos(num_genes, contador_movimientos):
    probabilidades = []  # Vector de probabilidades
    for _ in range(num_genes):
        probabilidades.append(0)
    probabilidades[2] = 1
    # Genera las probabilidades aleatorias
    # Normaliza el vector de probabilidades
    probabilidades = normalizar_vector(probabilidades)

    # Crea el cromosoma con probabilidades aleatorias y contador de movimientos
    cromosoma = {"genes": probabilidades, "contador_movimientos": contador_movimientos}

    return cromosoma


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


def seleccion_cromosomas(poblacion, porcentaje_seleccion=0.5):
    def probabilidad_acumulada():
        # Cálculo de la probabilidad acumulada para cada cromosoma
        total_fitness = sum(fitness)  # Suma de todos los valores de fitness
        prob_acumulada = [
            fit / total_fitness for fit in fitness
        ]  # Cálculo de la probabilidad acumulada
        return prob_acumulada

    def ultimo_cromosoma_menor_round():
        # Obtener el índice del último cromosoma con probabilidad acumulada menor o igual a un número aleatorio (round)
        rnd = random.random()
        for i, prob in enumerate(prob_acumulada):
            if prob >= rnd:
                return i
        return len(prob_acumulada) - 1

    def sacar_padres(porcentaje_seleccion):
        # Seleccionar los mejores cromosomas según el fitness
        num_padres = int(porcentaje_seleccion * len(cromosomas))
        sorted_indices = sorted(
            range(len(fitness)), key=lambda k: fitness[k]
        )  # Índices ordenados según el fitness
        padres = [
            cromosomas[i] for i in sorted_indices[:num_padres]
        ]  # Seleccionar los mejores cromosomas
        return padres

    # Lógica de la función principal
    fitness = obtener_fitness(
        cromosomas
    )  # Obtener los valores de fitness para los cromosomas
    prob_acumulada = probabilidad_acumulada()
    ultimo_crom_menor_round = ultimo_cromosoma_menor_round()
    padres = sacar_padres()

    return padres


def cruzar_cromosomas():
    return 0


def mutar_cromosomas():
    return 0


def llena_poblacion():
    return 0


def plot_cuadricula(poblacion):
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
                                        print(
                                            "Individuo {} ha llegado a la última columna y ha sido detectado".format(
                                                individuo_id
                                            )
                                        )
                                        print(
                                            "contador_movimientos: {}".format(
                                                individuo["contador_movimientos"]
                                            )
                                        )
                                    individuo[
                                        "contador_movimientos"
                                    ] -= 1  # Decrement contador_movimientos
                                    if individuo["contador_movimientos"] == 0:
                                        cuadricula_actual[fila][
                                            columna
                                        ] = 0  # Individuo se queda en su posición actual
                                else:
                                    cuadricula_actual[fila][columna] = individuo_id
                                    print(
                                        "Individuo {} se ha quedado en su posición actual".format(
                                            individuo_id
                                        )
                                    )
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
        ax.set_xlabel("Columna")
        ax.set_ylabel("Fila")
        plt.pause(0.1)

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
    plt.show()
    print("Fin del algoritmo genético")
    print("INDIVIDUOS QUE LLEGARON AL FINAL")
    print("================================")
    for i, individuo in enumerate(poblacion):
        if individuo["posicion_actual"][1] == tamano_tablero - 1:
            print(
                "Individuo {}: contador_movimientos: {}".format(
                    i + 1, individuo["contador_movimientos"]
                )
            )
            print("Individuo {}: genes: {}".format(i + 1, individuo["genes"]))
            print(
                "Individuo {}: posicion_actual: {}".format(
                    i + 1, individuo["posicion_actual"]
                )
            )
    print("================================")


def main():
    # Inicializar poblacion
    poblacion = crear_poblacion(20)
    # print(poblacion)

    plot_cuadricula(poblacion)
    print(f"\n{poblacion[0]['genes']} genes")

    # padres = seleccion_cromosomas(poblacion)
    # print(padres)

    # grafico2 = plot_cuadricula_ESPARTANA(poblacion, "Población final")


if __name__ == "__main__":
    main()
