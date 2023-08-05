from parallelsdk.proto import optimizer_defs_pb2

from enum import Enum
import logging


# Type of the routing model
class SchedulingModelType(Enum):
    EMPLOYEES_SCHEDULING = 1
    JOB_SHOP = 2

class SchedulingProblem:
    """Base class for scheduling problems.
    Derived classes can encapsulate Employees scheduling, JobShop, etc.,
    and add further constraints to the model.
    """
    model_type = None
    model_name = ""
    model_status = None

    def __init__(self, name, model_type):
        """Generates a new scheduling problem"""
        if not name.strip():
            err_msg = "SchedulingProblem - empty problem name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name

        # Set the type of problem to solve
        if not isinstance(model_type, SchedulingModelType):
            err_msg = "SchedulingProblem - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type

    def get_model_status(self):
        return self.status_to_string(self.model_status)

    def status_to_string(self, status):
        if status is None:
            return "SOLVER_UNKNOWN_STATUS"
        else:
            return optimizer_defs_pb2.OptimizerSolutionStatusProto.Name(status)

    def upload_proto_solution(self, solution_proto):
        # Upload the common parts of the solution and defer
        # problem specific details to sub-classes
        self.model_status = solution_proto.status
        self.upload_problem_proto_solution(solution_proto)

    def upload_problem_proto_solution(self, routing_model_solution_proto):
        raise Exception("SchedulingProblem - upload_problem_proto_solution: \
        to be implemented by derived classes")

    def name(self):
        """Returns the name of this routing problem"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        raise Exception("SchedulingProblem - to_protobuf")
