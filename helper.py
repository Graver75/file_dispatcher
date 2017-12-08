import socket
import json
import os
from uuid import uuid4
from io import BytesIO

from twisted.internet.protocol import Protocol


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

    @staticmethod
    def retrieve_file_from_ftp(name, ftp_client):
        proto = BufferingProtocol()
        d = ftp_client.retrieveFile(name, proto)
        d.addCallbacks(show_file, fail, callbackArgs=(proto,))



class BufferingProtocol(Protocol):
    """Simple utility class that holds all data written to it in a buffer."""
    def __init__(self):
        self.buffer = BytesIO()

    def dataReceived(self, data):
        self.buffer.write(data)

def show_file(result, buf):
    return buf.buffer.getvalue()

def fail(result, f):
    pass