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
