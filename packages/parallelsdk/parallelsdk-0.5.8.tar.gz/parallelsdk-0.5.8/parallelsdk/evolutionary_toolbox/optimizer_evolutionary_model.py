from parallelsdk import parallel_model
from parallelsdk.proto import evolutionary_model_pb2
from parallelsdk.evolutionary_toolbox.evolutionary_problem import EvolutionaryModelType
from parallelsdk.evolutionary_toolbox import genetic_problem

import logging


class OptimizerEvolutionaryModel(parallel_model.ParallelModel):
    """OptiLab Evolutionary model solved by back-end optimizers"""

    model_type = None
    model_name = ""
    evolutionary_model = None

    def __init__(self, name, model_type):
        """Generates a new evolutionary model"""
        if not name.strip():
            err_msg = "OptimizerEvolutionaryModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name

        if not isinstance(model_type, EvolutionaryModelType):
            err_msg = "OptimizerEvolutionaryModel - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if self.model_type is EvolutionaryModelType.GENETIC:
            self.evolutionary_model = genetic_problem.GeneticProblem(self.model_name)
        else:
            err_msg = "OptimizerEvolutionaryModel - unrecognized evolutionary model"
            logging.error(err_msg)
            raise Exception(err_msg)

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(evolutionary_model_pb2.EvolutionarySolutionProto.DESCRIPTOR):
            # Capture the protobuf solution
            sol_proto = evolutionary_model_pb2.EvolutionarySolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            err_msg = "OptimizerEvolutionaryModel - received an unrecognized back-end message"
            logging.error(err_msg)
            print(err_msg)

    def upload_proto_solution(self, evolutionary_model_solution_proto):
        # Upload the solution on the routing model itself
        self.evolutionary_model.upload_proto_solution(evolutionary_model_solution_proto)

    def get_model(self):
        """Returns the typed-instance of the evolutionary model"""
        return self.evolutionary_model

    def get_instance(self):
        """Returns the typed-instance of the evolutionary model"""
        return self.evolutionary_model

    def name(self):
        """Returns the name of this model"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be data_port_tool by derived classes"""
        return self.evolutionary_model.to_protobuf()
