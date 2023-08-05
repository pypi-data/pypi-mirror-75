from parallelsdk.proto import optimizer_model_pb2
from parallelsdk.proto import constraint_model_pb2
from . import cp_problem
from .CPModels.variable import Variable
from .CPModels.constraint import Constraint
from ortools.sat.python import cp_model


class CPSatProblem(cp_problem.CPProblem):
    def __init__(self, name):
        super().__init__(name)

        # Create OR-Tools CP-Sat
        self.__model = cp_model.CpModel()

        # Map of variables in the model
        self.__var_map = {}
        self.__var_idx_map = {}

        # Objective bound and value for optimization problems
        self.__is_optimization = False
        self.__objective_name = 'objective'
        self.__objective_value = None
        self.__objective_bound = None

    # Constructor for an integer variable
    def IntVar(self, lb, ub, name=''):
        var = Variable(self.__model, lb, ub, name)
        self.__add_variable_mapping(var)
        return var

    # Constructor for an 'expression' constraint
    def Constraint(self, expr):
        con = Constraint(self.__model, expr, "expression")
        return con

    ##########################
    #   Global constraints   #
    ##########################
    def AllDifferent(self, var_list):
        cp_con = self.__model.AddAllDifferent(var_list)
        con = Constraint(self.__model, cp_con, type='AllDifferent',
                         link='https://sofdem.github.io/gccat/gccat/Calldifferent.html')
        return con

    def Element(self, target, var_list, index):
        cp_con = self.__model.AddElement(index, var_list, target)
        con = Constraint(self.__model, cp_con, type='Element',
                         link='https://sofdem.github.io/gccat/gccat/Celement.html')
        return con

    def AbsEquality(self, target, var):
        cp_con = self.__model.AddAbsEquality(target, var)
        con = Constraint(self.__model, cp_con, type='AbsEquality',
                         link='https://sofdem.github.io/gccat/gccat/Cabs_value.html')
        return con

    def BoolAnd(self, literals):
        cp_con = self.__model.AddBoolAnd(literals)
        con = Constraint(self.__model, cp_con, type='BoolAnd',
                         link='https://sofdem.github.io/gccat/gccat/Cand.html')
        return con

    def BoolOr(self, literals):
        cp_con = self.__model.AddBoolOr(literals)
        con = Constraint(self.__model, cp_con, type='BoolOr',
                         link='https://sofdem.github.io/gccat/gccat/Cor.html')
        return con

    def Circuit(self, arcs):
        cp_con = self.__model.AddCircuit(arcs)
        con = Constraint(self.__model, cp_con, type='BoolXOr',
                         link='https://sofdem.github.io/gccat/gccat/Cxor.html',
                         info='An arc is a tuple (source_node, destination_node, literal). Enforces Hamiltonian path.')
        return con

    def Cumulative(self, intervals, demands, capacity):
        cp_con = self.__model.AddCumulative(intervals, demands, capacity)
        con = Constraint(self.__model, cp_con, type='Cumulative',
                         link='https://sofdem.github.io/gccat/gccat/Ccumulative.html')
        return con

    def DivEquality(self, target, num, denom):
        cp_con = self.__model.AddDivisionEquality(target, num, denom)
        con = Constraint(self.__model, cp_con, type='DivEquality')
        return con

    def Implication(self, var_a, var_b):
        cp_con = self.__model.AddImplication(var_a, var_b)
        con = Constraint(self.__model, cp_con, type='Implication')
        return con

    def MaxEquality(self, target, variables):
        cp_con = self.__model.AddMaxEquality(target, variables)
        con = Constraint(self.__model, cp_con, type='MaxEquality',
                         link='https://sofdem.github.io/gccat/gccat/Cmaximum.html')
        return con

    def MinEquality(self, target, variables):
        cp_con = self.__model.AddMinEquality(target, variables)
        con = Constraint(self.__model, cp_con, type='MinEquality',
                         link='https://sofdem.github.io/gccat/gccat/Cminimum.html')
        return con

    def ProdEquality(self, target, variables):
        cp_con = self.__model.AddMultiplicationEquality(target, variables)
        con = Constraint(self.__model, cp_con, type='ProdEquality',
                         link='https://sofdem.github.io/gccat/gccat/Cproduct_ctr.html')
        return con
    ##########################
    ##########################
    ##########################

    def get_infinity(self, positive=True):
        if positive:
            return cp_model.INT32_MAX
        else:
            return cp_model.INT32_MIN

    def enforce_con_if_var(self, con, var):
        con.enforce_if(var)

    def set_objective(self, obj, minimize=True):
        self.__is_optimization = True
        if minimize:
            self.__model.Minimize(obj)
        else:
            self.__model.Maximize(obj)

    def __add_variable_mapping(self, var):
        self.__var_map[var.Name()] = var
        self.__var_idx_map[len(self.__var_idx_map)] = var.Name()

    def __set_variable_value(self, var_idx, var_val):
        self.__var_map[self.__var_idx_map[var_idx]].set_value(var_val)

    def get_solution(self, solution_var_list=[]):
        solution = {}
        check_output_vars = len(solution_var_list) > 0
        for var_id in sorted(self.__var_map.keys()):
            if check_output_vars:
                if var_id in solution_var_list:
                    var = self.__var_map[var_id]
                    solution[var.Name()] = var.get_value()
            else:
                var = self.__var_map[var_id]
                solution[var.Name()] = var.get_value()
        if self.__is_optimization:
            solution[self.__objective_name] = self.__objective_value
            solution[self.__objective_name + '_bound'] = self.__objective_bound
        return solution

    def _upload_problem_proto_solution(self, solution_proto):
        var_idx = 0
        for var_val in solution_proto.cp_sat_solution.cp_solver_solution.solution:
            self.__set_variable_value(var_idx, var_val)
            var_idx += 1
        if self.__is_optimization:
            self.__objective_value = solution_proto.cp_sat_solution.cp_solver_solution.objective_value
            self.__objective_bound = solution_proto.cp_sat_solution.cp_solver_solution.best_objective_bound

    def to_protobuf(self):
        # Create a CP-Sat model
        optimizer_model = optimizer_model_pb2.OptimizerModel()
        optimizer_model.cp_model.model_id = self.name()
        optimizer_model.cp_model.cp_sat_model.cp_model.CopyFrom(self.__model.Proto())
        return optimizer_model
