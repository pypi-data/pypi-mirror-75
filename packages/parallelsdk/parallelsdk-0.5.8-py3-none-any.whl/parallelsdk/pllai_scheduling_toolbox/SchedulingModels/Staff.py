# The staff is a collection of employees, a "team"
from . import Employee


class Staff:
    id = 0

    def __init__(self, name, contact="N/A", department="N/A",):
        self.name = name
        self.contact = contact
        self.department = department
        self.staff_member_list = []
        self.id = Staff.id
        self.cost = 0
        self.cost_over_shift = 0
        self.shift_preference_map = {}
        self.schedule = {}
        Staff.id += 1

    def get_id(self):
        """Returns the unique id of this staff"""
        return self.id

    def get_name(self):
        """Returns the name of this staff/team"""
        return self.name

    def get_contact(self):
        """Returns the contact for this staff/team"""
        return self.contact

    def get_department(self):
        """Returns the department for this staff/team"""
        return self.department

    def set_staff_cost(self, cost):
        self.cost = cost

    def get_staff_cost(self):
        """Return the cost of this staff on one single shift
        without discounts"""
        return self.cost

    def get_staff_scheduling_cost(self):
        return self.cost_over_shift

    def is_scheduled(self, day, shift):
        """Returns true if this team works on given day/shift.
        Returns false otherwise"""
        if day in self.schedule.keys():
            if self.schedule[day] == shift:
                return True
        return False

    def add_schedule(self, day, shift):
        # Add cost of one shift to the scheduling cost
        self.cost_over_shift += self.get_staff_cost()
        self.schedule[day] = shift

        # Apply discount
        if day in self.shift_preference_map:
            preference_list = self.shift_preference_map[day]
            for preference in preference_list:
                # If the preference is satisfied, apply the discount
                if preference[0] == shift:
                    self.cost_over_shift -= preference[1]
                    return

    def add_staff_member(self, member, cost = 0):
        """Add a staff member to the staff. The caller can specify
        a cost for the member added to the staff"""
        if not isinstance(member, Employee.Employee):
            raise Exception("Staff - add_staff_member: invalid input type")
        self.staff_member_list.append(member)
        self.cost += cost

    def get_team_size(self):
        return len(self.staff_member_list)

    def print_staff(self):
        for member in self.staff_member_list:
            print(member)

    def get_shift_preference_map(self):
        """Returns the list of shift preferences"""
        return self.shift_preference_map

    def add_shift_preference(self, day, shift, discount=0):
        """Adds the preference for this Staff to work on specified
        day and shift. Further, it is possible to specify a discount
        on the staff cost that can be applied if the preference is
        satisfied by the scheduling"""
        if day in self.shift_preference_map:
            self.shift_preference_map[day].append([shift, discount])
        else:
            self.shift_preference_map[day] = [[shift, discount]]

    def print_schedule(self):
        sched = "==================\n"
        for day, shift in self.schedule.items():
            sched += "Day " + str(day) + "\n"
            sched += "Shift " + str(shift) + "\n"
            sched += "==================\n"
        print(sched)

    def __str__(self):
        info = "Staff:\n"
        info += "\tName: " + self.get_name()
        info += "\n\tContact: " + self.get_contact()
        info += "\n\tDepartment: " + self.get_department()
        info += "\n\tCost: " + str(self.get_staff_cost())
        info += "\nStaff members:\n"
        for employee in self.staff_member_list:
            info += employee.get_info()
            info += "\n=======\n"
        return info
