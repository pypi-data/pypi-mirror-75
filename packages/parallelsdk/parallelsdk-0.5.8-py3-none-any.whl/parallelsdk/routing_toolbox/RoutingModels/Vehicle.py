class Vehicle:
    uniqId = 0

    def __init__(self, name=None, load=0.0, capacity=float("inf")):
        self.name = name
        self.load = load
        self.capacity = capacity
        self.id = Vehicle.uniqId
        self.cost = 0
        Vehicle.uniqId += 1

    def get_id(self):
        """Returns the id of this vehicle"""
        return self.id

    def set_cost(self, cost=0):
        """Set cost per hour/mile of this vehicle"""
        self.cost = cost

    def get_cost(self):
        """Returns the cost of this vehicle per hour/mile"""
        return self.cost
