from . import optimizer_cp_model


def CPModel(model_name):
    """
    Builds and returns a new instance of a CP model.
    """
    cp_model = optimizer_cp_model.OptimizerCPModel(model_name)

    # Return the typed-instance of the model,
    # i.e., the actual TSP, VRP, etc. problem instance
    return cp_model
