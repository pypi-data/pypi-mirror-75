from parallelsdk import connector_factory
from parallelsdk.pllai_routing_toolbox import routing_problem
from . import scheduling_problem, employees_scheduling_to_vrp_connector


class SchedulingConnectorFactory(connector_factory.ConnectoryFactory):
    """Factory to build connectors linking Scheduling models"""

    def __init__(self, scheduling_type):
        super().__init__("SchedulingConnectorFactory", scheduling_type)
        self.source_type = scheduling_type

    def getConnector(self, model_type):
        source = self.get_source_type()
        if source == scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING:
            if model_type == routing_problem.RoutingModelType.VRP:
                return employees_scheduling_to_vrp_connector.EmployeesSchedulingToVRPConnector()

        raise Exception("SchedulingConnectorFactory: cannot connect " + type(source) + " and " + type(model_type))
