from parallelsdk.pllai_evolutionary_toolbox import evolutionary_problem, optimizer_evolutionary_model


def EvolutionaryModel(model_name, model_type):
    """Builds and returns a new instance of an Evolutionary model.
    The caller has to specify the type of model (e.g., Genetic algorithm, Ant colony).
    """
    if not isinstance(model_type, evolutionary_problem.EvolutionaryModelType):
        err_msg = "EvolutionaryModel - invalid model type " + type(model_type)
        raise Exception(err_msg)
    evolutionary_model = optimizer_evolutionary_model.OptimizerEvolutionaryModel(model_name, model_type)

    # Return the typed-instance of the model,
    # i.e., the actual Genetic Algorithm, Ant Colony, etc. problem instance
    return evolutionary_model

def BuildGeneticModel(model_name):
    """Builds and returns a new instance of a model for Genetic algorithms."""
    return EvolutionaryModel(model_name, evolutionary_problem.EvolutionaryModelType.GENETIC)
