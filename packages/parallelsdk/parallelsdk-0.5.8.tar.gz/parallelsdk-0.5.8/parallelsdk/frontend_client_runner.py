import ssl
import threading
import logging
try:
    import thread
except ImportError:
    import _thread as thread
import time
import queue
import websocket
from enum import Enum
from threading import Condition

DEBUG = False

K_CLIENT_LOG_OFF = "__CLIENT_LOG_OFF__"
K_ERROR_MESSAGE = "__ERROR_MESSAGE__"
K_HEALTH_MESSAGE = "__HEALTH_CHECK_STATUS_OK__"
K_INFO_MESSAGE = "__INFO_MESSAGE__"
K_PROCESS_COMPLETED = "__PROCESS_COMPLETED__"
K_SERVER_STATUS_ERROR_MESSAGE = "__SERVER_NON_REACHABLE__"


class ServerConnectionStatus(Enum):
    Alive = 1
    Unsure = 2
    NotReachable = 3

K_SERVER_IS_ALIVE = ServerConnectionStatus.NotReachable


class FrontendClientRunner:
    address = ""
    port = 0
    web_socket = None
    ws_url = ""

    def __init__(self, address, port, start_health_thread=True):
        # websocket.enableTrace(True)
        self.address = address
        self.port = port

        # Message queues
        self.queue = []
        self.health_queue = queue.Queue()

        # Current model being solved
        self.current_model = None

        # Condition variable to synchronize threads
        self.thread_run = True
        self.condition = Condition()

        # Start health thread
        self.start_health_thread = start_health_thread

        # Initialize the runner
        self.init_runner()

    def init_runner(self):
        self.ws_url = "ws://" + self.address + \
                      ":" + str(self.port) + "/proto_service"

    def is_online(self):
        global K_SERVER_IS_ALIVE
        return K_SERVER_IS_ALIVE is ServerConnectionStatus.Alive

    def connect_to_server(self):
        logging.info("Connecting to back-end server...")
        header = {
            'Sec-WebSocket-Protocol': 'graphql-subscriptions'
        }
        try:
            self.web_socket = websocket.WebSocketApp(self.ws_url,
                                                     header=header,
                                                     on_message = lambda ws, msg: self.on_message(ws, msg),
                                                     on_error   = lambda ws, msg: self.on_error(ws, msg),
                                                     on_close   = lambda ws:      self.on_close(ws),
                                                     on_open    = lambda ws:      self.on_open(ws))
            th = threading.Thread(target=self.connect_to_server_impl, daemon=True)
            th.start()

            # Start the health thread
            if self.start_health_thread:
                health_th = threading.Thread(target=self.health_monitor_system, daemon=True)
                health_th.start()

        except Exception as e:
            logging.exception(e)
            logging.error("Cannot connect to the back-end server, return")
            return False

        global K_SERVER_IS_ALIVE
        K_SERVER_IS_ALIVE = ServerConnectionStatus.Alive
        return True

    def health_monitor_system(self):
        time.sleep(1)

        global K_SERVER_IS_ALIVE
        while self.thread_run:
            try:
                self.health_queue.get(block=True, timeout=1)
                if DEBUG:
                    print("ALIVE CONNECTION")
                K_SERVER_IS_ALIVE = ServerConnectionStatus.Alive
            except:
                if K_SERVER_IS_ALIVE is ServerConnectionStatus.Alive:
                    if DEBUG:
                        print("UNSURE CONNECTION")
                    K_SERVER_IS_ALIVE = ServerConnectionStatus.Unsure
                else:
                    if DEBUG:
                        print("NO CONNECTION")
                    K_SERVER_IS_ALIVE = ServerConnectionStatus.NotReachable

            # Wait for next read
            time.sleep(2)

    def on_message(self, ws, message):
        global K_ERROR_MESSAGE
        global K_HEALTH_MESSAGE
        global K_INFO_MESSAGE
        global K_PROCESS_COMPLETED
        if isinstance(message, str) and message.startswith(K_HEALTH_MESSAGE):
            self.health_queue.put(message)
        elif isinstance(message, str) and message.startswith(K_ERROR_MESSAGE):
            logging.info(message)
            self.queue.append(message)
            return
        elif isinstance(message, str) and message.startswith(K_INFO_MESSAGE):
            logging.info(message)
        else:
            if self.current_model is None:
                msg = "The model is not set, return"
                logging.info(msg)
                if DEBUG:
                    print(msg)
                return

            if isinstance(message, str) and message.startswith(K_PROCESS_COMPLETED):
                self.condition.acquire()

                # Append the message to the queue
                self.queue.append(message)
                self.condition.notify()
                self.condition.release()
            else:
                # Proceed in parsing the protobuf message
                self.current_model.on_message(message)

    def on_error(self, ws, message):
        logging.error(message)

    def on_close(self, ws):
        logging.info("### Connection closed ###")

    def on_open(self, ws):
        logging.info("Client connected to back-end server")

    def connect_to_server_impl(self):
        # , sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY),)
        self.web_socket.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE,
                "check_hostname": False})

    def disconnect_from_server(self):
        # Initiate closing protocol with server
        global K_CLIENT_LOG_OFF
        if not self.web_socket or not self.web_socket.sock:
            return
        self.web_socket.sock.send(K_CLIENT_LOG_OFF)

        self.thread_run = False

        # Wait to logoff from server
        time.sleep(1)
        try:
            self.web_socket.close()
        except Exception as e:
            logging.exception(e)
            logging.info("Connection close and exception threw")
        finally:
            if DEBUG:
                print("### Connection closed ###")

    def send_proto_message_to_backend_server(self, proto_model):
        if self.web_socket is None:
            logging.error("Client not connected to back-end server, return")
            return False

        sent = self.web_socket.sock.send_binary(proto_model.SerializeToString())
        return sent

    def send_message_to_backend_server(self, model):
        if self.web_socket is None:
            logging.error("Client not connected to back-end server, return")
            return False

        # Set the current global model and send the request to the back-end
        # self.condition.acquire()
        self.current_model = model
        # self.condition.notify()
        # self.condition.release()
        sent = self.web_socket.sock.send_binary(model.serialize())
        return sent

    def get_message_from_backend_server(self):
        # TODO fix the below online check
        # if not self.is_online():
        #    return k_server_status_error_message
        self.condition.acquire()
        if not self.queue:
            self.condition.wait()
        msg = self.queue.pop(0)
        self.condition.notify()
        self.condition.release()
        return msg

    def wait_on_process_completion(self):
        msg = ""
        ctr = 0

        # Give time for connections to start-up
        global K_ERROR_MESSAGE
        global K_PROCESS_COMPLETED
        global K_SERVER_STATUS_ERROR_MESSAGE
        while not msg.startswith(K_PROCESS_COMPLETED):
            if msg.startswith(K_ERROR_MESSAGE):
                logging.error("Received error message from back-end server")
                return False
            if msg.startswith(K_SERVER_STATUS_ERROR_MESSAGE):
                logging.error("Back-end server seems to be offline")
                ctr += 1
                time.sleep(1)
                if ctr > 3:
                    return False
            msg = self.get_message_from_backend_server()

        # Give time for connections to close-up
        time.sleep(1)
        return True
