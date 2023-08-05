from parallelsdk.proto import optimizer_model_pb2


class DeploymentModel:
    def __init__(self, name=""):
        self.deployment_model_name = name
        self.optimizer_model = None

    def deploy_model(self, graph_model):
        self.optimizer_model = optimizer_model_pb2.OptimizerModel()
        self.optimizer_model.deployment_model.graph_model = bytes(graph_model, 'utf-8')

    def serialize(self):
        if not self.optimizer_model:
            return ""
        return self.optimizer_model.SerializeToString()
