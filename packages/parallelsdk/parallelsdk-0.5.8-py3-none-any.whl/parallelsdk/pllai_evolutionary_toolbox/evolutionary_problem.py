from parallelsdk.proto import optimizer_defs_pb2

from enum import Enum
import logging


# Type of the evolutionary model
class EvolutionaryModelType(Enum):
    GENETIC = 1
    ANT_COLONY = 2
    PARTICLE_SWARM = 3


class EvolutionaryProblem:
    """Base class for evolutionary problems.
    Derived classes can encapsulate GENETICs, ANT_COLONYs, etc.,
    and add further constraints to the model.
    """

    model_type = None
    model_name = ""

    def __init__(self, name, model_type):
        """Generates a new evolutionary problem"""
        if not name.strip():
            err_msg = "EvolutionaryProblem - empty problem name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.model_status = optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_UNKNOWN_STATUS
        self.random_seed = 0
        self.timeout_sec = 120
        self.stall_best = 0.0001
        self.multi_thread = False

        # Set the type of problem to solve
        if not isinstance(model_type, EvolutionaryModelType):
            err_msg = "EvolutionaryProblem - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type

    def set_random_seed(self, seed):
        self.random_seed = seed

    def get_random_seed(self):
        return self.random_seed

    def set_timeout_seconds(self, timeout_sec):
        self.timeout_sec = timeout_sec

    def get_timeout_seconds(self):
        return self.timeout_sec

    def set_stall_best(self, best_val):
        self.stall_best = best_val

    def get_stall_best(self):
        return self.stall_best

    def set_multi_thread(self, enabled):
        self.multi_thread = enabled

    def is_multi_thread(self):
        return self.multi_thread

    def is_solver_failed(self):
        """Returns true if the solver failed to find a solution.
        Returns false otherwise"""
        return self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL or \
               self.model_status == optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_FAIL_TIMEOUT

    def status_to_string(self, status):
        if status is None:
            return "SOLVER_UNKNOWN_STATUS"
        else:
            return optimizer_defs_pb2.OptimizerSolutionStatusProto.Name(status)

    def upload_proto_solution(self, solution_proto):
        # Upload the common parts of the solution and defer
        # problem specific details to sub-classes
        # Set model status
        self.model_status = solution_proto.status
        self.upload_problem_proto_solution(solution_proto)

    def upload_problem_proto_solution(self, solution_proto):
        raise Exception("EvolutionaryProblem - upload_problem_proto_solution: \
        to be implemented by derived classes")

    def name(self):
        """Returns the name of this routing problem"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        raise Exception("EvolutionaryProblem - toProtobuf")
