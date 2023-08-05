class ConnectoryFactory:
    """Factory to build connectors linking models"""

    def __init__(self, connector_factory_name, source_type):
        self.factory_name = connector_factory_name
        self.source_type = source_type

    def get_name(self):
        return self.factory_name

    def get_source_type(self):
        return self.source_type

    def getConnector(self, model_type):
        """Returns the connector connecting the source type model
        to a destination type model"""
        raise Exception("Implemented in derived classes")
