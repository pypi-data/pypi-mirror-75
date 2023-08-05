from parallelsdk import parallel_model
from parallelsdk.proto import data_model_pb2
from parallelsdk.data_toolbox.data_port_tools import DataModelType
from parallelsdk.data_toolbox import python_function_tool

import logging


class OptimizerDataPortTools(parallel_model.ParallelModel):
    model_type = None
    model_name = ""
    data_port_tool = None

    def __init__(self, name, model_type):
        if not name.strip():
            err_msg = "OptimizerDataPortTools - empty tool name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name

        if not isinstance(model_type, DataModelType):
            err_msg = "OptimizerDataPortTools - invalid tool type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if self.model_type is DataModelType.PYTHON_FCN:
            self.data_port_tool = python_function_tool.PythonFunctionTool(self.model_name)
        else:
            err_msg = "OptimizerDataPortTools - unrecognized tool"
            logging.error(err_msg)
            raise Exception(err_msg)

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(data_model_pb2.DataSolutionProto.DESCRIPTOR):

            # Capture the protobuf solution
            sol_proto = data_model_pb2.DataSolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            err_msg = "OptimizerDataPortTools - received an unrecognized back-end message"
            logging.error(err_msg)
            print(err_msg)

    def upload_proto_solution(self, solution_proto):
        self.data_port_tool.upload_proto_solution(solution_proto)

    def get_model(self):
        """Returns the typed-instance of the tool"""
        return self.data_port_tool

    def get_instance(self):
        """Returns the typed-instance of the tool"""
        return self.data_port_tool

    def get_solution(self):
        return self.data_port_tool.get_solution()

    def name(self):
        """Returns the name of this tool"""
        return self.model_name

    def serialize(self):
        proto = self.to_protobuf()
        return proto.SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overwritten by derived classes"""
        return self.data_port_tool.to_protobuf()
