from parallelsdk import parallel_model
from parallelsdk.proto import scheduling_model_pb2
from parallelsdk.scheduling_toolbox import employees_scheduling_problem, scheduling_problem
from parallelsdk.scheduling_toolbox.SchedulingModels.Employee import Employee
from parallelsdk.scheduling_toolbox.SchedulingModels.Staff import Staff

import logging


class OptimizerSchedulingModel(parallel_model.ParallelModel):
    """OptiLab Scheduling model solved by back-end optimizers"""

    model_type = None
    model_name = ""
    scheduling_model = None

    def __init__(self, name, model_type):
        """Generates a new scheduling model"""
        if not name.strip():
            err_msg = "OptimizerSchedulingModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name

        if not isinstance(model_type, scheduling_problem.SchedulingModelType):
            err_msg = "OptimizerSchedulingModel - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if self.model_type is scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING:
            self.scheduling_model = employees_scheduling_problem.EmployeesSchedulingProblem(self.model_name)
        else:
            err_msg = "OptimizerSchedulingModel - unrecognized routing model"
            logging.error(err_msg)
            raise Exception(err_msg)

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(scheduling_model_pb2.SchedulingSolutionProto.DESCRIPTOR):
            # Capture the protobuf solution
            sol_proto = scheduling_model_pb2.SchedulingSolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)
        else:
            msg = "OptimizerSchedulingModel - received an unrecognized back-end message"
            logging.error(err_msg)
            print(msg)

    def upload_proto_solution(self, scheduling_model_solution_proto):
        # Upload the solution on the scheduling model itself
        self.scheduling_model.upload_proto_solution(scheduling_model_solution_proto)

    def get_instance(self):
        """Returns the typed-instance of the scheduling model"""
        return self.scheduling_model

    def name(self):
        """Returns the name of this model"""
        return self.model_name

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        return self.scheduling_model.to_protobuf()

        # optimizer_model = optimizer_model_pb2.OptimizerModel()

        # Create a scheduling model and set its attributes:
        # 1 - set model name
        # optimizer_model.scheduling_model.model_id = self.model_name

        # 2 - set the scheduling model
        # if self.model_type is scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING:
        #    optimizer_model.scheduling_model.employee_scheduling_model.CopyFrom(self.scheduling_model.to_protobuf())
        # else:
        #    raise Exception("OptimizerSchedulingModel - unrecognized model type")

        # Return the model
        # return optimizer_model
