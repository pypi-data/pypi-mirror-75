from parallelsdk.routing_toolbox import routing_problem
from parallelsdk.scheduling_toolbox import scheduling_problem, scheduling_connector_factory


def get_connector_factory(model_type):
    """Returns the factory building objects connecting
    model_type models to other models"""
    if model_type == scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING:
        return scheduling_connector_factory.SchedulingConnectorFactory(model_type)
    else:
        raise Exception("get_connector_factory - cannot connect a block of type " + type(model_type))

def ModelConnector(from_model_type, to_model_type):
    """Builds and returns a new instance of a model connector class.
    The caller has to specify the type of models to connect
    """
    connectorFactory = get_connector_factory(from_model_type)
    return connectorFactory.getConnector(to_model_type)

def BuildEmployeesSchedulerToVehicleRoutingConverter():
    """Builds and returns a new instance of a converter
    to transform and connect Employees Scheduling problem to Vehicle Routing problems"""
    return ModelConnector(scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING,
                          routing_problem.RoutingModelType.VRP)
