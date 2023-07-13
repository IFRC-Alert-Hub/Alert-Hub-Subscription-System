import threading

from websockets.exceptions import ConnectionClosedOK, InvalidStatus

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
                self.websocket_connection.logger.info("The connection is closed!")
                break
            except TimeoutError:
                self.websocket_connection.logger.info(
                    "This connection is timeout, retry the connection....")
                WebsocketConnection.is_connected(False)
            except ConnectionRefusedError:
                self.websocket_connection.logger.info(
                    "The connection is refused, retry the connection....")
                WebsocketConnection.is_connected(False)
            except ConnectionAbortedError:
                self.websocket_connection.logger.info(
                    "The connection is aborted, retry the connection....")
                WebsocketConnection.is_connected(False)
            except InvalidStatus:
                self.websocket_connection.logger.info(
                    "The connection is rejected, retry the connection....")
                WebsocketConnection.is_connected(False)
            except ConnectionClosedOK:
                self.websocket_connection.logger.info("The connection is successfully closed.")
                WebsocketConnection.is_connected(False)
                break
            except ConnectionError:
                self.websocket_connection.logger.info("The connection is rejected.")
                self.websocket_connection.close_connection()
                break

    def stop(self):
        self.is_running.clear()

    def join(self, timeout=None):
        super().join(timeout)

    def shutdown(self):
        if self.websocket_connection.check_connected():
            print("Shutting down WebSocket connection...")
            self.websocket_connection.close_connection()
            self.stop()
        exit(0)
