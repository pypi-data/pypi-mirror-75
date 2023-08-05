from parallelsdk.pllai_routing_toolbox import routing_problem
from .RoutingModels import Vehicle
from parallelsdk.proto import optimizer_model_pb2


class TSPProblem(routing_problem.RoutingProblem):
    """Class encapsulating a generic Vehicle Routing Problem (TSP)"""

    num_vehicle = 1
    routing_solution = None

    def __init__(self, name=""):
        """Generates a new TSP instance"""
        super().__init__(name, routing_problem.RoutingModelType.TSP)

        self.add_vehicle( Vehicle(name="TSP vehicle") )

        self.routing_solution = None

    def add_vehicle(self, vehicle):
        if len(self.vehicles) > 0:
            raise Exception("TSP Problem: Vehicles cannot be added to TSP.")

    def add_depot(self, depot):
        if len(self.depots) > 0:
            raise Exception("TSP Problem: Depot already exists. Only one depot can be added to TSP.")
        else:
            super().add_depot(depot)

    def add_location(self, location):
        super().add_location(location)
        location.demand = 1.0

    def get_solution(self):
        """Returns the TSP tour"""
        return self.routing_solution

    def upload_problem_proto_solution(self, routing_model_solution_proto):
        if len(routing_model_solution_proto.single_route) != 1:
            raise Exception("TSPProblem - received invalid solution (invalid number of tours)")

        self.routing_solution = routing_problem.SingleRoute(
            routing_model_solution_proto.single_route[0].vehicle_id,
            routing_model_solution_proto.single_route[0].tot_route_distance)

        route = list(routing_model_solution_proto.single_route[0].route)
        self.routing_solution.set_route(route)

    def to_protobuf(self):
        # Create a TSP routing model
        optimizer_model = optimizer_model_pb2.OptimizerModel()

        # Set model name
        optimizer_model.routing_model.model_id = self.model_name

        # Set:
        # - depot
        optimizer_model.routing_model.tsp_model.depot = self.get_depots()[0].id

        # Set the distance matrix
        optimizer_model.routing_model.tsp_model.distance_matrix.rows = self.get_distance_matrixs_rows()
        optimizer_model.routing_model.tsp_model.distance_matrix.cols = self.get_distance_matrixs_cols()
        optimizer_model.routing_model.tsp_model.distance_matrix.multiplier_data = self.distance_matrix_mult
        for idx in range(self.distance_matrix.shape[0]):
            optimizer_model.routing_model.tsp_model.distance_matrix.data.extend(self.distance_matrix[idx].tolist())

        # Return the protobuf object
        return optimizer_model
