from parallelsdk.evolutionary_toolbox import evolutionary_problem
from parallelsdk.proto import evolutionary_model_pb2, optimizer_model_pb2
from parallelsdk.evolutionary_toolbox.EvolutionaryModels.Chromosome import Chromosome, ChromosomeType
from parallelsdk.evolutionary_toolbox.EvolutionaryModels.GeneticEnvironment import CrossoverType, MutationType, InitializationType, GeneticEnvironment, CustomEnvironment, StandardEnvironment, GeneticEnvironmentType


class GeneticProblem(evolutionary_problem.EvolutionaryProblem):
    """Class encapsulating a Genetic algorithm problem"""

    chromosome = None

    def __init__(self, name=""):
        """Generates a new Genetic algorithms model instance"""
        super().__init__(name, evolutionary_problem.EvolutionaryModelType.GENETIC)
        self.chromosome = None
        self.objective_value = 0.0
        self.mutation_rate = 0.2
        self.crossover_fraction = 0.7
        self.stall_max_gen = 10
        self.num_parents_on_crossover = 2
        self.objective_fcn_path = ""
        self.environment = None

        # TODO move the following to a base class
        self.population_size = 1
        self.num_generations = 1

    def build_chromosome(self, chromo_id, len, type):
        return Chromosome(chromo_id, len, type)

    def build_custom_environment(self):
        return CustomEnvironment(self.name())

    def build_standard_environment(self):
        return StandardEnvironment(self.name())

    def set_environment(self, env):
        if not isinstance(env, GeneticEnvironment):
            err_msg = "GeneticProblem - invalid object for environment: " + type(chromo)
            raise Exception(err_msg)
        self.environment = env

    def get_objective_value(self):
        """Returns the objective value"""
        return self.objective_value

    def set_chromosome(self, chromo):
        if not isinstance(chromo, Chromosome):
            err_msg = "GeneticProblem - invalid object for chromosome: " + type(chromo)
            raise Exception(err_msg)
        self.chromosome = chromo

    def get_chromosome(self):
        """Returns the chromosome being optimized"""
        return self.chromosome

    def set_objective_function_path(self, path):
        """Sets the path to the custom objective function
        to be read and build. The objective function is described
        as a C++ function with specified signature"""
        self.objective_fcn_path = path

    def get_objective_function_path(self):
        return self.objective_fcn_path

    def set_num_parents_for_crossover(self, num_parents):
        self.num_parents_on_crossover = num_parents

    def get_num_parents_for_crossover(self):
        return self.num_parents_on_crossover

    def set_num_generations(self, num):
        self.num_generations = num

    def get_num_generations(self):
        return self.num_generations

    def set_population_size(self, pop):
        self.population_size = pop

    def get_population_size(self):
        return self.population_size

    def set_stall_max_generations(self, max_gen):
        self.stall_max_gen = max_gen

    def get_stall_max_generations(self):
        return self.stall_max_gen

    def set_mutation_rate(self, rate):
        self.mutation_rate = rate

    def get_mutation_rate(self):
        return self.mutation_rate

    def set_crossover_fraction(self, cr_fraction):
        self.crossover_fraction = cr_fraction

    def get_crossover_fraction(self):
        return self.crossover_fraction

    def upload_problem_proto_solution(self, solution_proto):
        if not solution_proto.HasField("genetic_algorithm_solution"):
            raise Exception("GeneticProblem - invalid proto solution: not a genetic solution")

        # Set the objective function value
        self.objective_value = solution_proto.genetic_algorithm_solution.objective_value

        # Set the value of the chromosome
        idx = 0
        for val in solution_proto.genetic_algorithm_solution.chromosome_value:
            self.chromosome.set_chromosome_value(idx, val)
            idx = idx + 1

    def to_protobuf(self):
        # Create a Genetic model
        optimizer_model = optimizer_model_pb2.OptimizerModel()
        optimizer_model.evolutionary_model.model_id = self.name()

        optimizer_model.evolutionary_model.genetic_model.environment_name = self.name()
        optimizer_model.evolutionary_model.genetic_model.multithread = self.is_multi_thread()
        optimizer_model.evolutionary_model.genetic_model.parents_in_tournament = self.get_num_parents_for_crossover()
        optimizer_model.evolutionary_model.genetic_model.population_size = self.get_population_size()
        optimizer_model.evolutionary_model.genetic_model.num_generations = self.get_num_generations()
        optimizer_model.evolutionary_model.genetic_model.mutation_rate = self.get_mutation_rate()
        optimizer_model.evolutionary_model.genetic_model.crossover_fraction = self.get_crossover_fraction()
        optimizer_model.evolutionary_model.genetic_model.timeout_sec = self.get_timeout_seconds()
        optimizer_model.evolutionary_model.genetic_model.stall_best = self.get_stall_best()
        optimizer_model.evolutionary_model.genetic_model.stall_max_gen = self.get_stall_max_generations()
        optimizer_model.evolutionary_model.genetic_model.random_seed = self.get_random_seed()
        optimizer_model.evolutionary_model.genetic_model.objective_function_path = self.get_objective_function_path()

        # Set chromosome
        optimizer_model.evolutionary_model.genetic_model.chromosome.id = self.chromosome.get_id()
        optimizer_model.evolutionary_model.genetic_model.chromosome.lower_bound = self.chromosome.get_lower_bound()
        optimizer_model.evolutionary_model.genetic_model.chromosome.upper_bound = self.chromosome.get_upper_bound()
        if self.chromosome.get_type() is ChromosomeType.CHROMO_DOUBLE:
            optimizer_model.evolutionary_model.genetic_model.chromosome.type = evolutionary_model_pb2.ChromosomeProto.CHROMOSOME_DOUBLE
        else:
            optimizer_model.evolutionary_model.genetic_model.chromosome.type = evolutionary_model_pb2.ChromosomeProto.CHROMOSOME_INT
        optimizer_model.evolutionary_model.genetic_model.chromosome.dimensions.append(self.chromosome.get_length())

        # Set standard or custom environment
        if self.environment is None:
            raise Exception("GeneticProblem - to_protobuf: missing environment")
        if self.environment.get_type() is GeneticEnvironmentType.STANDARD:
            crs = self.environment.get_crossover_type()
            crsProto = None
            if crs is CrossoverType.ORDER_1:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.ORDER_1
            elif crs is CrossoverType.EDGE_RECOMBINATION:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.EDGE_RECOMBINATION
            elif crs is CrossoverType.PMX:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.PMX
            elif crs is CrossoverType.ORDER_MULTIPLE:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.ORDER_MULTIPLE
            elif crs is CrossoverType.CYCLE:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.CYCLE
            elif crs is CrossoverType.DIRECT_INSERTION:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.DIRECT_INSERTION
            optimizer_model.evolutionary_model.genetic_model.standard_environment.crossover = crsProto

            mut = self.environment.get_mutation_type()
            mutProto = None
            if mut is MutationType.RANDOM_SLIDE:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.RANDOM_SLIDE
            elif mut is MutationType.INVERSION:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.INVERSION
            elif mut is MutationType.INSERTION:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.INSERTION
            elif mut is MutationType.SINGLE_SWAP:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.SINGLE_SWAP
            elif mut is MutationType.SCRAMBLE:
                crsProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.SCRAMBLE
            optimizer_model.evolutionary_model.genetic_model.standard_environment.mutation = mutProto

            init = self.environment.get_initialization_type()
            initProto = None
            if init is InitializationType.RANDOM:
                initProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.RANDOM
            elif init is InitializationType.PERMUTATION:
                initProto = evolutionary_model_pb2.StandardGeneticEnvironmentProto.PERMUTATION
            optimizer_model.evolutionary_model.genetic_model.standard_environment.initialization = initProto
        elif self.environment.get_type() is GeneticEnvironmentType.CUSTOM:
            for path in self.environment.get_path_to_environment():
                optimizer_model.evolutionary_model.genetic_model.custom_environment.environment_path.append(path)

        # Return the protobuf object
        return optimizer_model
