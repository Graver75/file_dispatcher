import socket
import json
import os
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

    @staticmethod
    def presend(mes):
        return bytes(json.dumps(mes) + '\n', 'utf8')

    @staticmethod
    def get_MD5(file):
        # TODO: implement
        pass

    @staticmethod
    def get_stats(path):
        pass

    @staticmethod
    def list_files(path):
        return os.listdir(path=path)
