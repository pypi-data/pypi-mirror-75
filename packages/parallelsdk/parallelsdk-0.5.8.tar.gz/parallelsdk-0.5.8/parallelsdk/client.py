from . import frontend_client_runner
import time
import logging

DEBUG = True


class ParallelClient:
    address = ""
    port = -1
    client_runner = None

    def __init__(self, address, port=8080, heath_check=True):
        self.address = address
        self.port = port
        self.start_health_check = heath_check

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect Parallel front-end interface to the service"""
        self.client_runner = frontend_client_runner.FrontendClientRunner(self.address, self.port,
                                                                         start_health_thread=self.start_health_check)

        if DEBUG:
            print('Connecting front-end to Parallel platform...')

        connected = self.client_runner.connect_to_server()
        time.sleep(1.5)

        if not connected:
            logging.error("Cannot connect to the server")
        return connected

    def disconnect(self):
        """Disconnect Parallel front-end interface from the service"""
        self.client_runner.disconnect_from_server()

    def is_client_online(self):
        return self.client_runner.is_online()

    def run_optimizer_from_proto(self, proto_model):
        if self.client_runner is None:
            logging.error("The client is not connected to the server")
            return False

        return self.client_runner.send_proto_message_to_backend_server(proto_model)

    def run_optimizer(self, model):
        """Sends the given model to the Parallel back-end service.

        Creates back-end optimizers and run the service on the serialized
        model provided by the caller.
        """
        if self.client_runner is None:
            logging.error("The client is not connected to the server")
            return False

        return self.client_runner.send_message_to_backend_server(model)

    def run_optimizer_synch_from_proto(self, proto_model):
        if self.client_runner is None:
            logging.error("The client is not connected to the server")
            return False

        sent = self.client_runner.send_proto_message_to_backend_server(proto_model)
        if not sent:
            return False

        # Block the current thread until the solving process is completed
        return self.client_runner.wait_on_process_completion()

    def run_optimizer_synch(self, model):
        """Sends the given model to the Parallel back-end service.

        Creates back-end optimizers and run the service on the serialized
        model provided by the caller.
        This is the synchronous blocking version of the run_optimizer(...) method.
        This call blocks until the model has been completely solved.
        """
        if self.client_runner is None:
            logging.error("The client is not connected to the server")
            return False

        sent = self.client_runner.send_message_to_backend_server(model)
        if not sent:
            return False

        # Block the current thread until the solving process is completed
        return self.client_runner.wait_on_process_completion()
