from . import optimizer_routing_model, routing_problem


def RoutingModel(model_name, model_type):
    """Builds and returns a new instance of a Routing model.
    The caller has to specify the type of model (e.g., TSP, VRP).
    By default, the model type represent a Vehicle Routing Problem (VRP).
    """
    if not isinstance(model_type, routing_problem.RoutingModelType):
        err_msg = "RoutingModel - invalid model type " + type(model_type)
        raise Exception(err_msg)
    routing_model = optimizer_routing_model.OptimizerRoutingModel(model_name, model_type)

    # Return the typed-instance of the model,
    # i.e., the actual TSP, VRP, etc. problem instance
    return routing_model


def BuildTSP(model_name):
    """Builds and returns a new instance of a model for TSP."""
    return RoutingModel(model_name, routing_problem.RoutingModelType.TSP)


def BuildVRP(model_name):
    """Builds and returns a new instance of a model for VRP."""
    return RoutingModel(model_name, routing_problem.RoutingModelType.VRP)
