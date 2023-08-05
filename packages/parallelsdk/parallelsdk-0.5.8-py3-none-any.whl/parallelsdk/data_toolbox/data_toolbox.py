from parallelsdk.data_toolbox import data_port_tools, optimizer_data_port_tools


def DataAndPorts(model_name, model_type):
    if not isinstance(model_type, data_port_tools.DataModelType):
        err_msg = "DataAndPorts - invalid model type " + type(model_type)
        raise Exception(err_msg)
    data_model = optimizer_data_port_tools.OptimizerDataPortTools(model_name, model_type)

    # Return the typed-instance of the model
    return data_model


def BuildPythonFunctionTool(model_name):
    return DataAndPorts(model_name, data_port_tools.DataModelType.PYTHON_FCN)
