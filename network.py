# network.py

import socket
import threading
import re


class Network:
    def __init__(self, host: str, port: int, receive_callback=None):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_callback = receive_callback

    def connect(self, username: str):
        try:
            self.client_socket.connect((self.host, self.port))
            message = self.format_message("SETNAME", username)
            self._send_message(message)
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if self.receive_callback:
                    self.receive_callback(message)
            except Exception as e:
                print(f"Receiving Error: {e}")
                self.client_socket.close()
                break

    def _send_message(self, message: str):
        try:
            self.client_socket.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Sending Error: {e}")

    def subscribe(self, channel: str):
        message = self.format_message("SUBSCRIBE", channel)
        self._send_message(message)

    def unsubscribe(self, channel: str):
        message = self.format_message("UNSUBSCRIBE", channel)
        self._send_message(message)

    # send message
    def send_message(self, channel: str, message: str):
        message = self.format_message("MESSAGE", channel, message)
        self._send_message(message)

    def disconnect(self):
        self.client_socket.close()

    @staticmethod
    def format_message(command: str, *args: str):
        """
        Formats a message with the given command and arguments,
        escaping special characters.
        """
        escaped_args = [arg.replace("\\", "\\\\") for arg in args]
        return f"{command}\\x" + "\\x".join(escaped_args)
