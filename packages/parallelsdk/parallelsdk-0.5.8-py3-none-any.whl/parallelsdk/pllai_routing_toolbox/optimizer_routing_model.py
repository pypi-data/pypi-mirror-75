from parallelsdk.proto import optilab_pb2, routing_model_pb2
from parallelsdk import parallel_model
from .routing_problem import RoutingEngineType, RoutingModelType
from . import vrp_problem, tsp_problem
from .RoutingModels.Location import Location, Depot
from .RoutingModels.Vehicle import Vehicle

import numpy as np
import logging


class OptimizerRoutingModel(parallel_model.ParallelModel):
    """OptiLab Routing model solved by back-end optimizers"""

    model_type = None
    engine_type = None
    model_name = ""
    routing_model = None

    def __init__(self, name, model_type):
        """Generates a new routing model"""
        if not name.strip():
            err_msg = "OptimizerRoutingModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.engine_type = RoutingEngineType.CP_ENGINE

        if not isinstance(model_type, RoutingModelType):
            err_msg = "OptimizerRoutingModel - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if self.model_type is RoutingModelType.TSP:
            self.routing_model = tsp_problem.TSPProblem(self.model_name)
        elif self.model_type is RoutingModelType.VRP:
            self.routing_model = vrp_problem.VRPProblem(self.model_name)
        else:
            err_msg = "OptimizerRoutingModel - unrecognized routing model"
            logging.error(err_msg)
            raise Exception(err_msg)

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(
                optilab_pb2.OptimizerSolutionRep.DESCRIPTOR):
            # JSON solutions are printed verbatim on the screen.
            # @note DEPRECATED
            sol_msg = optilab_pb2.OptimizerSolutionRep()
            optilab_reply_message.details.Unpack(sol_msg)
            print(sol_msg.solution)
        elif optilab_reply_message.details.Is(routing_model_pb2.RoutingSolutionProto.DESCRIPTOR):
            # Capture the protobuf solution
            sol_proto = routing_model_pb2.RoutingSolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            msg = "OptimizerRoutingModel - received an unrecognized back-end message"
            logging.error(err_msg)
            print(msg)

    def upload_proto_solution(self, routing_model_solution_proto):
        # Upload the solution on the routing model itself
        self.routing_model.upload_proto_solution(routing_model_solution_proto)

    def is_solver_failed(self):
        """Returns true if the solver failed to find a solution, false otherwise"""
        return self.get_model().is_solver_failed()

    def get_model(self):
        """Returns the typed-instance of the routing model"""
        return self.routing_model

    def get_solution(self):
        return self.routing_model.get_solution()

    def set_engine_type(self, engine_type):
        if not isinstance(model_type, RoutingEngineType):
            err_msg = "RoutingModel - SetEngineType: invalid engine type " + \
                type(engine_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.engine_type = engine_type

    def name(self):
        """Returns the name of this model"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def AddLocation(self, position, demand=0.0):
        if isinstance(position, Location) == True:
            position.set_id(Location.uniqId)
            Location.uniqId += 1
            self.routing_model.add_location( position )
            return

        if isinstance(position, np.ndarray) == False:
            raise Exception("numpy array expected for position")
        if len(position.shape) != 1:
            raise Exception("position shape has to be 1d array")

        self.routing_model.add_location( Location(position, demand) )

    def AddDepot(self, position):
        if isinstance(position, Depot) == True:
            position.set_id(Location.uniqId)
            Location.uniqId += 1
            self.routing_model.add_depot( position )
            return

        if isinstance(position, np.ndarray) == False:
            raise Exception("numpy array expected for position")
        if len(position.shape) != 1:
            raise Exception("position shape has to be 1d array")

        self.routing_model.add_depot( Depot(position) )

    def AddVehicleInstance(self, vehicle):
        if isinstance(vehicle, Vehicle):
            self.routing_model.add_vehicle( vehicle )
        else:
            raise Exception("AddVehicle - expected a Vehicle type")

    def AddVehicle(self, name, load, capacity):
        self.routing_model.add_vehicle(Vehicle(name, load, capacity))

    def SetDistanceMatrix(self, dist_matrix, time_matrix=False, mult_data=1):
        self.routing_model.set_distance_matrix(dist_matrix, time_matrix, mult_data)

    def InferDistanceMatrix(self, metric="euclidean"):
        self.routing_model.infer_distance_matrix(metric)

    def SetTimeWindows(self, time_windows):
        self.routing_model.set_time_windows(time_windows)

    def Clear(self):
        """Clear internal state"""
        Location.uniqId = 0
        if self.model_type is RoutingModelType.TSP:
            self.routing_model = tsp_problem.TSPProblem(self.model_name)
        elif self.model_type is RoutingModelType.VRP:
            self.routing_model = vrp_problem.VRPProblem(self.model_name)
        else:
            err_msg = "OptimizerRoutingModel - unrecognized routing model on Clear"
            logging.error(err_msg)
            raise Exception(err_msg)

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        print("Calling to_protobuf in optimizer routing model")
        return self.routing_model.to_protobuf()
