from parallelsdk.data_toolbox import data_port_tools
from parallelsdk.proto import data_model_pb2, optimizer_model_pb2

import logging


class PythonFunctionTool(data_port_tools.DataAndPorts):
    def __init__(self, name=""):
        super().__init__(name, data_port_tools.DataModelType.PYTHON_FCN)

        # Create a Python function model
        self._python_fcn_model = optimizer_model_pb2.OptimizerModel()
        self._python_fcn_model.data_model.model_id = self.name()
        self._output = []

    def add_entry_fcn_name(self, fcn_name):
        self._python_fcn_model.data_model.python_model.entry_fcn_name = fcn_name

    def get_entry_fcn_name(self):
        return self._python_fcn_model.data_model.python_model.entry_fcn_name

    def add_entry_module_name(self, module_name):
        self._python_fcn_model.data_model.python_model.entry_module_name = module_name

    def get_entry_module_name(self):
        return self._python_fcn_model.data_model.python_model.entry_module_name

    def add_environment_path(self, path):
        self._python_fcn_model.data_model.python_model.python_file_path.append(path)

    def get_environment_path(self):
        return self._python_fcn_model.data_model.python_model.python_file_path[0]

    def get_output(self):
        return self._output

    def infer_type_from_value(self, val):
        if isinstance(val, int):
            return "int"
        elif isinstance(val, float):
            return "double"
        elif isinstance(val, bool):
            return "bool"
        elif isinstance(val, str):
            return "string"
        elif isinstance(val, bytes):
            return "bytes"
        else:
            return "string"

    def set_typed_value(self, typed_val, val, proto_type):
        if not proto_type:
            proto_type = self.infer_type_from_value(val)
        if proto_type == "double":
            typed_val.double_arg = val
            return True
        elif proto_type == "float":
            typed_val.float_arg = val
            return True
        elif proto_type == "int":
            typed_val.int_arg = val
            return True
        elif proto_type == "uint":
            typed_val.uint_arg = val
            return True
        elif proto_type == "bool":
            typed_val.bool_arg = val
            return True
        elif proto_type == "string":
            typed_val.string_arg = val
            return True
        elif proto_type == "byte":
            typed_val.bytes_arg = val
            return True
        elif proto_type == "bytes":
            typed_val.bytes_arg = val
            return True
        else:
            return False

    def set_output_typed_value(self, typed_val, proto_type):
        if proto_type == "double":
            typed_val.double_arg = 0.0
            return True
        elif proto_type == "float":
            typed_val.float_arg = 0.0
            return True
        elif proto_type == "int":
            typed_val.int_arg = 0
            return True
        elif proto_type == "uint":
            typed_val.uint_arg = 0
            return True
        elif proto_type == "bool":
            typed_val.bool_arg = True
            return True
        elif proto_type == "string":
            typed_val.string_arg = "Placeholder"
            return True
        elif proto_type == "byte":
            typed_val.bytes_arg = "Placeholder"
            return True
        elif proto_type == "bytes":
            typed_val.bytes_arg = "Placeholder"
            return True
        else:
            return False

    def clear_input_arguments(self):
        """
        Clears all input arguments from the function protobuf message.
        """
        del self._python_fcn_model.data_model.python_model.input_args[:]

    def add_input_argument(self, val, data_type=''):
        fcn_arg = self._python_fcn_model.data_model.python_model.input_args.add()
        if isinstance(val, list):
            # List of values
            for x in val:
                typed_val = fcn_arg.argument.add()
                if not self.set_typed_value(typed_val, x, data_type):
                    err_msg = "PythonFunctionTool - invalid list input data type"
                    logging.error(err_msg)
                    raise Exception(err_msg)
        else:
            # Scalar value
            typed_val = fcn_arg.argument.add()
            if not self.set_typed_value(typed_val, val, data_type):
                err_msg = "PythonFunctionTool - invalid scalar input data type"
                logging.error(err_msg)
                raise Exception(err_msg)

    def add_input_descriptor(self, data_type, is_list):
        """ Similar to add_output_descriptor, this method is used to store the data-type of
        the inputs received by the Python function. This is used when deploying a model
        to setup the proper inputs"""
        # TODO Implement this method
        pass

    def add_output_argument(self, data_type, is_list):
        """ For the output, val is a placeholder.
            The only thing that actually matters is whether or not val is a list and
            the data_type
        """
        fcn_arg = self._python_fcn_model.data_model.python_model.output_args.add()
        if is_list:
            # List of values
            for _ in range(2):
                typed_val = fcn_arg.argument.add()
                if not self.set_output_typed_value(typed_val, data_type):
                    err_msg = "PythonFunctionTool - invalid list output data type"
                    logging.error(err_msg)
                    raise Exception(err_msg)
        else:
            # Scalar value
            typed_val = fcn_arg.argument.add()
            if not self.set_output_typed_value(typed_val, data_type):
                err_msg = "PythonFunctionTool - invalid scalar output data type"
                logging.error(err_msg)
                raise Exception(err_msg)

    def get_arg_typed_value(self, val):
        # val is PythonFcnTypedValue
        if val.HasField("double_arg"):
            return val.double_arg
        elif val.HasField("float_arg"):
            return val.float_arg
        elif val.HasField("int_arg"):
            return val.int_arg
        elif val.HasField("uint_arg"):
            return val.uint_arg
        elif val.HasField("bool_arg"):
            return val.bool_arg
        elif val.HasField("string_arg"):
            return val.string_arg
        elif val.HasField("bytes_arg"):
            return val.bytes_arg
        else:
            return None

    def upload_proto_solution(self, solution_proto):
        if not solution_proto.HasField("python_fcn_solution"):
            raise Exception("PythonFunctionTool - invalid proto solution: not a python function tool solution")

        # Build the output w.r.t. the declared output
        num_outputs = len(self._python_fcn_model.data_model.python_model.output_args)
        assert num_outputs >= len(solution_proto.python_fcn_solution.output)

        # Clear previous output
        del self._output[:]

        idx = 0
        for out_val in solution_proto.python_fcn_solution.output:
            # out_val is a PythonFcnArgument
            out_descriptor = self._python_fcn_model.data_model.python_model.output_args[idx]
            idx += 1

            out_list = []
            for val in out_val.argument:
                # val is a PythonFcnTypedValue
                out_list.append(self.get_arg_typed_value(val))
            if len(out_descriptor.argument) == 1:
                self._output.append(out_list[0])
            else:
                self._output.append(out_list)

    def to_protobuf(self):
        # Return the protobuf object
        return self._python_fcn_model
