import threading

import websockets
from websockets.exceptions import ConnectionClosedOK,InvalidStatus

from subscription_manager_dir.establish_websockets_connection import WebsocketConnection


class WebsocketThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_running = threading.Event()
        self.websocket_connection = WebsocketConnection()

    def run(self):
        while True:
            # Run the WebSocket connection
            try:
                self.websocket_connection.establish_websocket_connection()
                break
            except KeyboardInterrupt:  # pylint: disable=broad-except
                self.websocket_connection.close_connection()
                print("The connection is closed!")
                break
            except TimeoutError:
                print("This connection is timeout, retry the connection....")
                WebsocketConnection.isConnected(False)
            except ConnectionRefusedError:
                print("The connection is refused, retry the connection....")
                WebsocketConnection.isConnected(False)
            except ConnectionAbortedError:
                print("The connection is aborted, retry the connection....")
                WebsocketConnection.isConnected(False)
            except InvalidStatus:
                print("The connection is rejected, retry the connection....")
                WebsocketConnection.isConnected(False)
            except ConnectionClosedOK:
                print("The connection is successfully closed.")
                WebsocketConnection.isConnected(False)
                break
            except ConnectionError:
                print("The connection is rejected.")
                self.websocket_connection.close_connection()
                break

    def stop(self):
        self.is_running.clear()

    def join(self, timeout=None):
        super().join(timeout)

    def shutdown(self):
        if self.websocket_connection.checkConnected():
            print("Shutting down WebSocket connection...")
            self.websocket_connection.close_connection()
            self.stop()
        exit(0)