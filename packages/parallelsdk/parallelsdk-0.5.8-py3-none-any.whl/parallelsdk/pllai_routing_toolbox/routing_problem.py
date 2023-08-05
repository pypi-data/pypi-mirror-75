from parallelsdk.proto import optimizer_defs_pb2
from .RoutingModels.Vehicle import Vehicle
from .RoutingModels.Location import Location, Depot

from sklearn.metrics import pairwise_distances
import numpy as np


from enum import Enum
import logging


# Type of the routing model
class RoutingModelType(Enum):
    VRP = 1
    TSP = 2


# The "RoutingEngineType" sets the type of engine
# to be used to solve a routing model of type "RoutingModelType".
# For example, a VRP model can be solved by an
# engine implementing "ACTOR_POLICY_VRP", i.e., using
# an actor executing a policy learned with Reinforcement Learning.
# @note not all combinations of model types and engine
# types are valid combinations
class RoutingEngineType(Enum):
    ACTOR_POLICY_VRP = 1
    CP_ENGINE = 2


class SingleRoute:
    """Class describing the route of vehicle"""
    # Route description
    vehicle_id = 0
    route = []
    tot_route_distance = -1

    def __init__(self, v_id, tot_distance, vehicle=None):
        self.vehicle_id = v_id
        self.tot_route_distance = tot_distance
        self.vehicle = vehicle
        self.route = []

    def get_vehicle_id(self):
        return self.vehicle_id

    def get_vehicle(self):
        return self.vehicle

    def set_route(self, route):
        if not isinstance(route, list):
            raise Exception("SingleRoute - set_route: input argument must be a list")
        self.route = route

    def get_route(self):
        return self.route

    def get_total_distance(self):
        return self.tot_route_distance

    def get_total_cost(self):
        if self.vehicle is not None:
            if not isinstance(self.vehicle, Vehicle):
                raise Exception("SingleRoute - get_total_cost: invalid vehicle type")
            return self.get_total_distance() * self.vehicle.get_cost()
        return 0


class RoutingProblem:
    """Base class for routing problems.
    Derived classes can encapsulate TSPs, VRPs, etc.,
    and add further constraints to the model.
    """

    engine_type = None
    model_type = None
    model_name = ""
    is_time_matrix = False
    depot_node = -1
    total_distance = -1

    def __init__(self, name, model_type):
        """Generates a new routing problem"""
        if not name.strip():
            err_msg = "RoutingProblem - empty problem name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.model_status = optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_UNKNOWN_STATUS

        self.vehicles = []
        self.locations = []
        self.depots = []

        # Total distance traveled
        self.total_distance = -1

        # By default, use the CP engine for solving routing
        self.engine_type = RoutingEngineType.CP_ENGINE
        self.distance_matrix = []

        # Distance matrix.
        # @note distance is "relative": it can be an actual distance in space
        # or a time matrix
        self.distance_matrix_rows = -1
        self.distance_matrix_cols = -1
        self.distance_matrix_mult = 1

        # Set the type of problem to solve
        if not isinstance(model_type, RoutingModelType):
            err_msg = "RoutingProblem - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type

    def is_solver_failed(self):
        """Returns true if the solver failed to find a solution.
        Returns false otherwise"""
        return self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL or \
               self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL_TIMEOUT

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise Exception("RoutingProblem: Vehicle object expected, but received %s" % (str(type(vehicle))))
        self.vehicles.append( vehicle )

    def add_location(self, location):
        if not isinstance(location, Location):
            raise Exception("RoutingProblem: Location object expected, but received %s" % (str(type(location))))
        self.locations.append(location)

    def add_depot(self, depot):
        if not isinstance(depot, Depot):
            raise Exception("RoutingProblem: Depot object expected, but received %s" % (str(type(depot))))
        self.depots.append(depot)

    def get_model_status(self):
        return self.status_to_string(self.model_status)

    def get_depots(self):
        """Returns the number of locations"""
        return self.depots

    def get_locations(self):
        """Returns the number of locations"""
        return self.locations

    def get_vehicles(self):
        """Returns the number of vehicles"""
        return self.vehicles

    def get_total_load(self):
        """Returns the total routing load"""
        return sum( [v.load for v in self.vehicles] )

    def get_demands(self):
        """Returns the demand list"""
        demands = [ 0 for l in self.depots ]
        demands.extend( [ l.demand for l in self.locations ] )
        return demands

    def get_capacities(self):
        """Returns the demand list"""
        return [ v.capacity for v in self.vehicles ]

    def status_to_string(self, status):
        if status is None:
            return "SOLVER_UNKNOWN_STATUS"
        else:
            return optimizer_defs_pb2.OptimizerSolutionStatusProto.Name(status)

    def get_total_distance(self):
        """Returns the total routing distance"""
        return self.total_distance

    def upload_proto_solution(self, routing_model_solution_proto):
        # Upload the common parts of the solution and defer
        # problem specific details to sub-classes
        # Set model status
        self.model_status = routing_model_solution_proto.status
        self.total_distance = routing_model_solution_proto.tot_distance
        self.upload_problem_proto_solution(routing_model_solution_proto)

    def upload_problem_proto_solution(self, routing_model_solution_proto):
        raise Exception("RoutingProblem - upload_problem_proto_solution: \
        to be implemented by derived classes")

    def set_engine_type(self, engine_type):
        if not isinstance(model_type, RoutingEngineType):
            err_msg = "RoutingProblem - SetEngineType: invalid engine type " + \
                type(engine_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.engine_type = engine_type

    def name(self):
        """Returns the name of this routing problem"""
        return self.model_name

    def infer_distance_matrix(self, metric="euclidean"):
        positions = np.zeros( (len(self.locations) + len(self.depots), self.locations[0].position.shape[0]) )
        idx = 0
        for d in self.depots:
            positions[idx] = d.position
            idx += 1

        idx = 0
        for l in self.locations:
            positions[idx] = l.position
            idx += 1

        self.distance_matrix = pairwise_distances( positions, metric=metric )
        self.distance_matrix_rows = self.distance_matrix.shape[0]
        self.distance_matrix_cols = self.distance_matrix.shape[1]
        self.distance_matrix_mult = 1

    def set_distance_matrix(self, dist_matrix, time_matrix=False, mult_data=1):
        """Sets the distance matrix. The mutliplier parameter is used
        to scale up/down each entry since only finite values are allowed.
        The time_matrix flag indicates whether or not this is a time matrix
        rather than a distance (spatial) matrix.
        """
        self.distance_matrix = dist_matrix
        self.is_time_matrix = time_matrix
        self.distance_matrix_mult = mult_data
        rows = len(self.distance_matrix)

        # Check distance matrix:
        # must be a non-empty, square matrix
        if rows == 0:
            err_msg = "RoutingProblem - set_distance_matrix: invalid matrix (empty)"
            logging.error(err_msg)
            raise Exception(err_msg)
        for idx in range(len(self.distance_matrix)):
            if (not isinstance(self.distance_matrix[idx], list)) or len(self.distance_matrix[idx]) != rows:
                err_msg = "RoutingProblem - set_distance_matrix: invalid matrix size " + \
                    str(len(self.distance_matrix[idx]))
                logging.error(err_msg)
                raise Exception(err_msg)

        # Set distance matrix size
        self.distance_matrix_rows = rows
        self.distance_matrix_cols = rows

    def get_distance_matrix(self):
        """Returns the distance matrix"""
        return self.distance_matrix

    def get_distance_matrixs_rows(self):
        """Returns the number of rows of the distance matrix"""
        return self.distance_matrix_rows

    def get_distance_matrixs_cols(self):
        """Returns the number of colums of the distance matrix"""
        return self.distance_matrix_cols

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        raise Exception("RoutingModel - toProtobuf")
