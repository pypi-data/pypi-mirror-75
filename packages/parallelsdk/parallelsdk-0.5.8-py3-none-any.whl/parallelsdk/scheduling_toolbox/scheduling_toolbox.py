from . import scheduling_problem, optimizer_scheduling_model


def SchedulingModel(model_name, model_type):
    """Builds and returns a new instance of a Scheduling model.
    The caller has to specify the type of model (e.g., EMPLOYEES_SCHEDULING, JOB_SHOP).
    """
    if not isinstance(model_type, scheduling_problem.SchedulingModelType):
        err_msg = "SchedulingModel - invalid model type " + type(model_type)
        raise Exception(err_msg)
    scheduling_model = optimizer_scheduling_model.OptimizerSchedulingModel(model_name, model_type)

    # Return the typed-instance of the model,
    # i.e., the actual EmployeesScheduling, JobShop, etc. problem instance
    return scheduling_model


def BuildEmployeesScheduler(model_name):
    """Builds and returns a new instance of a model for the
    Employees Scheduling problem."""
    return SchedulingModel(model_name, scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING)
