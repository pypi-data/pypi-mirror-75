class Location:
    uniqId = 0

    def __init__(self, position, demand=0.0):
        self.position = position
        self.demand = demand
        self.id = Location.uniqId
        Location.uniqId += 1

    def set_id(self, id):
        """Override the existing location id with the given input id"""
        self.id = id


class Depot(Location):

    def __init__(self, position):
        super().__init__(position)
