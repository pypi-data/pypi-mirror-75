from parallelsdk import parallel_model
from parallelsdk.proto import optilab_pb2, constraint_model_pb2
from . import cp_sat_problem
import logging


class OptimizerCPModel(parallel_model.ParallelModel):
    """
    Builds and returns a new instance of a CP model.
    """

    def __init__(self, name):
        """Generates a new CP model"""
        if not name.strip():
            err_msg = "OptimizerCPModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.cp_model = cp_sat_problem.CPSatProblem(self.model_name)

    def name(self):
        """Returns the name of this model"""
        return self.model_name

    def get_model(self):
        """Returns the typed-instance of the CP model"""
        return self.cp_model

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(constraint_model_pb2.ConstraintSolutionProto.DESCRIPTOR):

            # Capture the protobuf solution
            sol_proto = constraint_model_pb2.ConstraintSolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            err_msg = "OptimizerCPModel - received an unrecognized back-end message"
            logging.error(err_msg)
            print(err_msg)

    def upload_proto_solution(self, solution_proto):
        # Upload the solution on the CP model itself
        self.cp_model.upload_proto_solution(solution_proto)

    def get_solution(self):
        return self.cp_model.get_solution()

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        return self.cp_model.to_protobuf()
