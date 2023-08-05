from enum import Enum
import numpy as np
import sys


class ChromosomeType(Enum):
    """Type of Chromosome"""
    CHROMO_DOUBLE = 1
    CHROMO_INT = 2


class Chromosome:
    """
    In genetic algorithms, a chromosome (also sometimes called a genotype) is a
    set of parameters which define a proposed solution to the problem that the
    genetic algorithm is trying to solve. The set of all solutions is known as the
    population.
    The chromosome is often represented as a binary string, although a wide
    variety of other data structures are also used
    """
    def __init__(self, id, chromo_length, chromo_type):
        if not isinstance(chromo_type, ChromosomeType):
            raise Exception("Chromosome - invalid chromosome type")
        self.id = id
        self.type = chromo_type
        self.length = chromo_length
        self.lower_bound = -sys.float_info.max
        self.upper_bound = sys.float_info.max
        self.chromo = np.zeros(self.length)

    def set_chromosome_value(self, idx, val):
        self.chromo[idx] = val

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_length(self):
        return self.length

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def get_chromosome(self):
        return self.chromo

    def set_lower_bound(self, lb):
        if lb > self.upper_bound:
            raise Exception("Chromosome - set_lower_bound: invalid lower bound")
        self.lower_bound = lb

    def set_upper_bound(self, ub):
        if ub < self.lower_bound:
            raise Exception("Chromosome - set_upper_bound: invalid upper bound")
        self.upper_bound = ub

    def get_info(self):
        info = "Chromosome:\n\tid: " + self.get_id()
        info += "\n\tlower bound: " + str(self.get_lower_bound())
        info += "\n\tupper bound: " + str(self.get_upper_bound())
        info += "\n\tlength: " + str(self.get_length())
        info += "\n\tchromosome:\n"
        info += str(self.get_chromosome())
        return info

    def __str__(self):
        return self.get_info()
