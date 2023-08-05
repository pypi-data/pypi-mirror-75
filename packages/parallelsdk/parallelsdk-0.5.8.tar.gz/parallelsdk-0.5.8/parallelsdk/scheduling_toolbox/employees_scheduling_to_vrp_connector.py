from parallelsdk import connector
from . import employees_scheduling_problem
from parallelsdk.routing_toolbox import optimizer_routing_model

from parallelsdk.routing_toolbox.RoutingModels import Vehicle
from .SchedulingModels.Staff import Staff

import numpy as np


class EmployeesSchedulingToVRPConnector(connector.Connectory):
    """Factory to build connectors linking Employees Scheduling to VRP models"""

    def __init__(self):
        super().__init__("EmployeesSchedulingToVRPConnector")
        self.source_model = None
        self.destination_model = None
        self.num_routes = 0
        self.staff_vehicle_map = {}
        self.shift_location_map = {}
        self.solution_list = {}

    def map_staff_vehicle(self, staff, vehicle_list, depot):
        """Maps the staff members to the vehicles in the vehicle list.
        Specifies a depot location from where each staff member starts his/her shift"""
        if not isinstance(staff, Staff):
            raise Exception("EmployeesSchedulingToVRPConnector - invalid type: expected Staff, received ", type(staff))
        if isinstance(depot, np.ndarray) == False:
            raise("EmployeesSchedulingToVRPConnector - invalid type: numpy array expected for depot")
        for vehicle in vehicle_list:
            if not isinstance(vehicle, Vehicle):
                raise Exception("EmployeesSchedulingToVRPConnector - invalid type: expected Vehicle, received ", type(vehicle))
        self.staff_vehicle_map[staff.get_name()] = [depot, vehicle_list]

    def map_shift_location(self, day, shift, location_list):
        """Maps the schedule (day/shift) to the locations to reach on each shift"""
        if day in self.shift_location_map.keys():
            self.shift_location_map[day][shift] = location_list
        else:
            self.shift_location_map[day] = {}
            self.shift_location_map[day][shift] = location_list

    def get_map_depot(self, day, shift):
        """Returns the depot to start from for routing given the specified
        day and shift"""
        team = self.source_model.get_team_on_schedule(day, shift)
        if team:
            return self.staff_vehicle_map[team][0]
        raise Exception("EmployeesSchedulingToVRPConnector - no depot set on day ", day, " shift ", shift)

    def get_map_locations(self, day, shift):
        """Returns the locations to go to for routing given the specified
        day and shift"""
        return self.shift_location_map[day][shift]

    def get_map_vehicles(self, day, shift):
        """Returns the vehicles to use to go to the specified location on the given
        day and shift"""
        team = self.source_model.get_team_on_schedule(day, shift)
        if team:
            return self.staff_vehicle_map[team][1]
        raise Exception("EmployeesSchedulingToVRPConnector - no vehicles set on day ", day, " shift ", shift)

    def print_scheduling(self):
        for day, solution in self.solution_list.items():
            print("===================")
            print("Route on day: ", day)
            for shift_route in solution:
                print("Shift: ", shift_route[0])
                for route in shift_route[1]:
                    print("Route: " + str(route.get_route()))
                    print("Total distance: " + str(route.get_total_distance()))

    def connect(self, source_model, destination_model):
        """Connects source model to the destination model"""
        if not isinstance(source_model, employees_scheduling_problem.EmployeesSchedulingProblem):
            raise Exception("EmployeesSchedulingToVRPConnector - invalid source model type")
        if not isinstance(destination_model, optimizer_routing_model.OptimizerRoutingModel):
            raise Exception("EmployeesSchedulingToVRPConnector - invalid destination model type")
        self.source_model = source_model
        self.destination_model = destination_model
        print("Connecting Employees Scheduling model with VRP.")
        print("Route scheduling will be performed over:")
        days = self.source_model.get_schedule_num_days()
        shifts = self.source_model.get_shift_per_day()
        self.num_routes = days * shifts
        print("- Days: ", days)
        print("- Shift per day: ", shifts)
        print("For a total of ", self.num_routes, " possible routes.")

    def run(self, optimizer):
        """Runs the connector"""

        # Prepare the routes
        days = self.source_model.get_schedule_num_days()
        shifts = self.source_model.get_shift_per_day()
        for d in range(days):
            for s in range(shifts):
                self.destination_model.Clear()
                self.destination_model.AddDepot(self.get_map_depot(d, s))

                for loc in self.get_map_locations(d, s):
                    self.destination_model.AddLocation(loc)

                for vehicle in self.get_map_vehicles(d, s):
                    self.destination_model.AddVehicleInstance(vehicle)

                # Get distance matrix
                self.destination_model.InferDistanceMatrix()

                # Run the optimizer synchronously
                optimizer.run_optimizer_synch(self.destination_model)

                # Store the solution
                if not self.destination_model.is_solver_failed():
                    if d in self.solution_list.keys():
                        self.solution_list[d].append([s, self.destination_model.get_solution()])
                    else:
                        self.solution_list[d] = [[s, self.destination_model.get_solution()]]
                else:
                    print("Cannot find a solution for day ", d, " and shift ", s)
