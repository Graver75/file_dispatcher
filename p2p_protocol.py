from twisted.internet.protocol import Protocol

import json


class P2PProtocol(Protocol):
    def __init__(self):
        self.state = "HELLO"
        self.remote_node_id = None

    def connectionMade(self):
        print('Connection made from', self.transport.getHost())

    # TODO: fix reason
    def connectionLost(self, reason=True):
        if self.remote_node_id in self.factory.peers:
            self.factory.peers.pop(self.remote_node_id)
        print(self.remote_node_id, 'disconnected')

    def dataReceived(self, data):
        for line in data.splitlines():
            line = line.strip()
            if self.state == "HELLO":
                self.handle_hello(line)
                self.state = "READY"

    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_node_id = hello["node_id"]
        if self.remote_node_id == self.factory.node_id:
            print('Connection loop')
            self.transport.loseConnection()
        else:
            print(self.remote_node_id, 'connected')
            self.factory.peers[self.remote_node_id] = self.transport.getPeer()

    def send_hello(self):
        hello = json.dumps({'node_id': self.factory.node_id, 'msgtype': 'hello'})
        self.transport.write(hello + "\n")