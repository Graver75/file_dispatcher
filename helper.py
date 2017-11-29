import socket
from uuid import uuid4


class Helper:
    @staticmethod
    def generate_node_id():
        return str(uuid4())

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]