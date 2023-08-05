from enum import Enum


class GeneticEnvironmentType(Enum):
    STANDARD = 1
    CUSTOM = 2


class CrossoverType(Enum):
  	ORDER_1 = 1;
  	EDGE_RECOMBINATION = 2;
  	PMX = 3;
  	ORDER_MULTIPLE = 4;
  	CYCLE = 5;
  	DIRECT_INSERTION = 6;


class MutationType(Enum):
  	RANDOM_SLIDE = 1;
  	INVERSION = 2;
  	INSERTION = 3;
  	SINGLE_SWAP = 4;
  	SCRAMBLE = 5;


class InitializationType(Enum):
  	RANDOM = 1;
  	PERMUTATION = 2;


class GeneticEnvironment:
    def __init__(self, id, type):
        if not isinstance(type, GeneticEnvironmentType):
            err_msg = "GeneticEnvironment - invalid environment type: " + type(type)
            raise Exception(err_msg)
        self.id = id
        self.type = type

    def get_type(self):
        return self.type


class StandardEnvironment(GeneticEnvironment):
    def __init__(self, id):
        super().__init__(id, GeneticEnvironmentType.STANDARD)
        self.crossover_type = None
        self.mutation_type = None
        self.initialization = None

    def set_crossover_type(self, crossover):
        if not isinstance(crossover, CrossoverType):
            err_msg = "GeneticProblem - invalid crossover type: " + type(crossover)
            raise Exception(err_msg)
        self.crossover_type = crossover

    def set_mutation_type(self, mutation):
        if not isinstance(mutation, MutationType):
            err_msg = "GeneticProblem - invalid mutation type: " + type(mutation)
            raise Exception(err_msg)
        self.mutation_type = crossover

    def set_initialization_type(self, initialization):
        if not isinstance(initialization, InitializationType):
            err_msg = "GeneticProblem - invalid initialization type: " + type(initialization)
            raise Exception(err_msg)
        self.initialization = initialization

    def get_crossover_type(self):
        return self.crossover_type

    def get_mutation_type(self):
        return self.mutation_type

    def get_initialization_type(self):
        return self.initialization


class CustomEnvironment(GeneticEnvironment):
    def __init__(self, id):
        super().__init__(id, GeneticEnvironmentType.CUSTOM)
        self.path_to_environment = []

    def add_path_to_environment(self, path):
        self.path_to_environment.append(path)

    def clear_path_to_environment(self):
        self.path_to_environment.clear()

    def get_path_to_environment(self):
        return self.path_to_environment
