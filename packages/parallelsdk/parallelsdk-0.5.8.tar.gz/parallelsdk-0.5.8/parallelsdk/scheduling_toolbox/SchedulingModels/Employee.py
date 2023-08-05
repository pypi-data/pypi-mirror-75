class Employee:
    id = 0

    def __init__(self, name, gender="N/A", number="N/A", department="N/A", city="N/A"):
        self.name = name
        self.gender = gender
        self.number = number
        self.department = department
        self.city = city
        self.shift_list = []
        self.id = Employee.id
        Employee.id += 1

    def print_shift(self):
        for shift in self.shift_list:
            print("Day:\t", shift[0])
            print("Shift:\t", shift[1])
            print("Satifies:\t", shift[2])
            print("==============")

    def add_shift(self, shift):
        self.shift_list.append(shift)

    def set_gender(self, gender):
        self.gender = gender

    def set_number(self, number):
        self.number = number

    def set_department(self, department):
        self.department = department

    def set_city(self, city):
        self.city = city

    def get_num_shifts(self):
        return len(self.shift_list)

    def get_shift(self, shift_num):
        return self.shift_list[shift_num]

    def get_shift(self):
        return self.shift_list

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_gender(self):
        return self.gender

    def get_number(self):
        return self.number

    def get_department(self):
        return self.department

    def get_city(self):
        return self.city

    def get_info(self):
        emp_info = "Employee:\n\tname: " + self.get_name()
        emp_info += "\n\tgender: " + self.get_gender()
        emp_info += "\n\tnumber: " + self.get_number()
        emp_info += "\n\tdepartment: " + self.get_department()
        emp_info += "\n\tcity: " + self.get_city()
        return emp_info

    def __str__(self):
        return self.get_info()
