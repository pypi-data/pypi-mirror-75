from . import routing_problem
from parallelsdk.proto import optimizer_model_pb2


class VRPSingleRoute(routing_problem.SingleRoute):
    load = []
    tot_load = -1

    def __init__(self, v_id, tot_distance, vehicle=None):
        super().__init__(v_id, tot_distance, vehicle)

    def set_load_on_nodes(self, load_nodes):
        if not isinstance(load_nodes, list):
            raise Exception("VRPSingleRoute - set_load_on_nodes: input argument must be a list")
        self.load = load_nodes

    def get_load_on_nodes(self):
        """Returns the list of loads per node"""
        return self.load

    def set_tot_load(self, load):
        self.tot_load = load

    def get_tot_load(self):
        return self.tot_load

class VRPProblem(routing_problem.RoutingProblem):
    """Class encapsulating a generic Vehicle Routing Problem (VRP)"""

    routing_solution = []

    def __init__(self, name=""):
        """Generates a new VRP instance"""
        super().__init__(name, routing_problem.RoutingModelType.VRP)
        self.routing_solution = []
        self.time_windows = None

    def get_solution(self):
        """Returns the routes of each vehicle in the VRP"""
        return self.routing_solution

    def get_solution_vehicle_cost(self):
        """Returns the total cost of the solution given the cost of the vehicles"""
        tot_cost = 0
        for route in self.get_solution():
            tot_cost += route.get_total_cost()
        return tot_cost

    def set_time_windows(self, time_windows):
        if not isinstance(time_windows, list):
            raise Exception("time windows must be a list")

        self.time_windows = time_windows

    def upload_problem_proto_solution(self, routing_model_solution_proto):
        self.total_load = routing_model_solution_proto.tot_load

        # Upload the routes of each vehicles
        for proto_route in routing_model_solution_proto.single_route:
            vehicle = None
            vehicle_list = self.get_vehicles()
            for v in vehicle_list:
                if proto_route.vehicle_id == v.get_id():
                    vehicle = v
                    break
            route = VRPSingleRoute(proto_route.vehicle_id, proto_route.tot_route_distance, vehicle)
            route.set_tot_load(proto_route.tot_load)
            route.set_load_on_nodes( list(proto_route.load) )
            route.set_route( list(proto_route.route) )
            self.routing_solution.append(route)

    def to_protobuf(self):
        # Create a VRP routing model
        optimizer_model = optimizer_model_pb2.OptimizerModel()
        optimizer_model.routing_model.model_id = self.model_name

        # Set:
        # - demand
        # - capacity
        # - number of vehicles
        # - depot
        optimizer_model.routing_model.vrp_model.demand.extend( self.get_demands() )
        optimizer_model.routing_model.vrp_model.capacity.extend( self.get_capacities() )
        optimizer_model.routing_model.vrp_model.num_vehicle = len(self.get_vehicles())
        optimizer_model.routing_model.vrp_model.depot = self.get_depots()[0].id

        # Set the distance matrix
        optimizer_model.routing_model.vrp_model.distance_matrix.rows = self.get_distance_matrixs_rows()
        optimizer_model.routing_model.vrp_model.distance_matrix.cols = self.get_distance_matrixs_cols()
        optimizer_model.routing_model.vrp_model.distance_matrix.multiplier_data = self.distance_matrix_mult
        for idx in range(len(self.distance_matrix)):
            optimizer_model.routing_model.vrp_model.distance_matrix.data.extend(self.distance_matrix[idx])

        if self.time_windows:
            initial_times = [ x[0] for x in self.time_windows ]
            end_times = [ x[1] for x in self.time_windows ]

            optimizer_model.routing_model.vrp_model.time_windows.initial_times.extend( initial_times )
            optimizer_model.routing_model.vrp_model.time_windows.end_times.extend( end_times )
            optimizer_model.routing_model.vrp_model.time_windows.waiting_time = 30
            optimizer_model.routing_model.vrp_model.time_windows.max_time_per_vehicle = 100

        # Return the protobuf object
        return optimizer_model
