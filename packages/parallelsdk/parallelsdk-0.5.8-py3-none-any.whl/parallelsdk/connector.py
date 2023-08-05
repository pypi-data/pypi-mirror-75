class Connectory:
    """Base class for connector objects"""

    def __init__(self, connector_name):
        self.name = connector_name

    def get_name(self):
        return self.name

    def connect(self, source_model, destination_model):
        """Connects source model to the destination model"""
        raise Exception("Implemented in derived classes")

    def run(self, optimizer):
        """Runs the connector"""
        raise Exception("Implemented in derived classes")
