from ortools.sat.python import cp_model


class Constraint:
    """
    Class encapsulating a CP constraint.
    The Constraint class is not implemented as "is-a" but
    as "has-a" holding a constraint object from OR-Tools cp_model
    """
    def __init__(self, model, expr_or_constraint, type='', link='', info=''):
        self.__id = id(self)
        self.__name = 'c_' + str(self.__id)
        self.__type = type
        self.__link = link
        self.__info = info
        if isinstance(expr_or_constraint, cp_model.Constraint):
            self.__con = expr_or_constraint
        else:
            self.__con = model.Add(expr_or_constraint)

    def enforce_if(self, var):
        self.__con.OnlyEnforceIf(var)

    def to_string(self):
        con_str = 'Constraint:\n'
        con_str += '\tid: ' + self.__name + '\n'
        if self.__type:
            con_str += '\ttype: ' + self.__type + '\n'
        if self.__info:
            con_str += '\tinfo: ' + self.__info + '\n'
        if self.__link:
            con_str += '\tinfo: ' + self.__link + '\n'
        return con_str

    def __str__(self):
        return self.to_string()
