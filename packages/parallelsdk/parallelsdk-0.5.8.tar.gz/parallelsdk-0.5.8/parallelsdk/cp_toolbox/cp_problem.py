import logging
from parallelsdk.proto import optimizer_defs_pb2


class CPProblem:
    """
    Base class for Constraint Programming problems.
    Derived classes can encapsulate CPSat, CP-Gecode, etc.,
    and add further constraints to the model.
    """

    def __init__(self, name):
        """Generates a new CP problem"""
        if not name.strip():
            err_msg = "RoutingProblem - empty problem name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.model_status = optimizer_defs_pb2.OptimizerSolutionStatusProto.OPT_SOLVER_UNKNOWN_STATUS

    def name(self):
        """Returns the name of this CP problem"""
        return self.model_name

    def status_to_string(self):
        return optimizer_defs_pb2.OptimizerSolutionStatusProto.Name(self.model_status)

    def upload_proto_solution(self, solution_proto):
        """Upload basic information from the solution proto message.
        Defer the actual solution value upload to the derived classes."""
        self.model_status = solution_proto.status
        self._upload_problem_proto_solution(solution_proto)

    def get_solution(self):
        raise NotImplemented()

    def to_protobuf(self):
        raise NotImplemented()

    def _upload_problem_proto_solution(self, solution_proto):
        raise NotImplemented()
