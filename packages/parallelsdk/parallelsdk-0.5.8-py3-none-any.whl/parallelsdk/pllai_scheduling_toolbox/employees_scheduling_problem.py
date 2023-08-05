from parallelsdk.proto import optimizer_model_pb2
from parallelsdk.proto import scheduling_model_pb2
from . import scheduling_problem
from .SchedulingModels.Staff import Staff


class EmployeesSchedulingProblem(scheduling_problem.SchedulingProblem):
    """Class encapsulating an Employees scheduling problem.
    In an Employees scheduling problem there are a number of employees,
    a number of days, and a number of shifts per day. The problem is to
    assign employees to shifts to cover all days considering fairness.
    In other words, constraints to ensure that shifts are scheduled fairly
    among employees and preferences are respected."""

    staff_db = None
    num_shift_per_day = 0
    num_days = 0
    shift_preference_list = []
    staff_schedule = []

    def __init__(self, name=""):
        """Generates a new Employees scheduling model instance"""
        super().__init__(name, scheduling_problem.SchedulingModelType.EMPLOYEES_SCHEDULING)
        self.staff_db = dict()
        self.num_shift_per_day = 0
        self.num_days = 0

    def add_staff(self, staff):
        if isinstance(staff, Staff) == False:
            raise Exception("EmployeesSchedulingProblem: Staff object expected, but received %s" %(str(type(staff))))

        # Add the staff to the map
        self.staff_db[staff.get_name()] = staff

    def get_staff(self, name):
        return self.staff_db.get(name)

    def set_schedule_num_days(self, days):
        """Sets the length of the schedule in number of days"""
        self.num_days = days

    def set_shift_per_day(self, spd):
        """Sets the number of shifts within a day"""
        self.num_shift_per_day = spd

    def get_schedule_num_days(self):
        return self.num_days

    def get_shift_per_day(self):
        return self.num_shift_per_day

    def get_num_teams(self):
        return len(self.staff_db)

    def get_team_from_id(self, id):
        for ename, staff in self.staff_db.items():
            if staff.get_id() == id:
                return staff
        raise Exception("get_team_from_id: no ID found")

    def get_team_on_schedule(self, day, shift):
        """Returns the staff/team name working on the given day/shift"""
        for ename, staff in self.staff_db.items():
            if staff.is_scheduled(day, shift):
                return ename
        return ""

    def print_schedule(self):
        for ename, staff in self.staff_db.items():
            print("Team: ", ename)
            staff.print_schedule()

    def upload_problem_proto_solution(self, scheduling_model_solution_proto):
        """Uploads the solution returned from the back-end optimizer"""
        if not scheduling_model_solution_proto.HasField("employee_scheduling_solution"):
            err_msg = "EmployeesSchedulingProblem - invalid solution type"
            raise Exception(err_msg)

        solution_proto = scheduling_model_solution_proto.employee_scheduling_solution
        for day_shift in solution_proto.day_schedule:
            for ds in day_shift.shift_schedule:
                # Set the same information on the employee
                staff = self.get_team_from_id(ds.employee_id)
                staff.add_schedule(day_shift.day, ds.shift)

    def to_protobuf(self):
        # Create a employees scheduling model
        optimizer_model = optimizer_model_pb2.OptimizerModel()
        optimizer_model.scheduling_model.model_id = self.model_name
        # sched_proto = scheduling_model_pb2.EmployeeSchedulingModelProto()

        # Set:
        # - number of employees
        optimizer_model.scheduling_model.employee_scheduling_model.num_employees = self.get_num_teams()

        # - number of shifts per day
        optimizer_model.scheduling_model.employee_scheduling_model.num_shift_per_day = self.get_shift_per_day()

        # - number of days
        optimizer_model.scheduling_model.employee_scheduling_model.num_days = self.get_schedule_num_days()

        # - shift preferences
        for ename, staff in self.staff_db.items():
            for day, shift in staff.get_shift_preference_map().items():
                shift_pref = scheduling_model_pb2.EmployeeSchedulingPreferenceProto()
                shift_pref.employee_id = staff.get_id()
                shift_pref.day = day
                shift_pref.shift = shift[0][0]
                optimizer_model.scheduling_model.employee_scheduling_model.shift_preference_list.append(shift_pref)

        # Return the protobuf object
        return optimizer_model
