from parallelsdk.proto import optimizer_defs_pb2

from enum import Enum
import logging


# Type of the evolutionary model
class DataModelType(Enum):
    PYTHON_FCN = 1


class DataAndPorts:
    """Base class for data and ports tools."""

    model_type = None
    model_name = ""

    def __init__(self, name, model_type):
        if not name.strip():
            err_msg = "DataAndPorts - empty tool name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.model_status = optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_UNKNOWN_STATUS

        # Set the type of problem to solve
        if not isinstance(model_type, DataModelType):
            err_msg = "DataAndPorts - invalid tool type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type

    def is_solver_failed(self):
        return self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL or \
               self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL_TIMEOUT

    def status_to_string(self, status):
        if status is None:
            return "SOLVER_UNKNOWN_STATUS"
        else:
            return optimizer_defs_pb2.OptimizerSolutionStatusProto.Name(status)

    def upload_proto_solution(self, solution_proto):
        self.model_status = solution_proto.status
        self.upload_problem_proto_solution(solution_proto)

    def upload_problem_proto_solution(self, solution_proto):
        raise Exception("DataAndPorts - upload_problem_proto_solution: \
        to be implemented by derived classes")

    def name(self):
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        raise Exception("DataAndPorts - toProtobuf")
