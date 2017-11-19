from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from time import time

import json


class P2PProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.state = "HELLO"
        self.remote_node_id = None
        self.lc_ping = LoopingCall(self.send_ping)
        self.last_ping = None

    def connectionMade(self):
        print('Connection made from', self.transport.getHost())
        self.send_hello()

    # TODO: fix reason
    def connectionLost(self, reason=True):
        if self.remote_node_id in self.factory.peers:
            self.factory.peers.pop(self.remote_node_id)
            self.lc_ping.stop()
        print(self.remote_node_id, 'disconnected')

    def dataReceived(self, data):
        for line in data.splitlines():
            line = line.strip()
            msg_type = json.loads(line)["msgtype"]
            if self.state == "HELLO" or msg_type == "HELLO":
                self.handle_hello(line)
                self.state = "READY"
            elif msg_type == "ping":
                self.handle_ping()
            elif msg_type == "pong":
                self.handle_pong()

    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_node_id = hello["node_id"]
        if self.remote_node_id == self.factory.node_id:
            print('Connection loop')
            self.transport.loseConnection()
        else:
            print(self.remote_node_id, 'connected')
            self.factory.peers[self.remote_node_id] = self.transport.getPeer()
            self.lc_ping.start(60)

    def send_hello(self):
        hello = json.dumps({'node_id': self.factory.node_id, 'msgtype': 'hello'})
        self.transport.write(bytes(hello + '\n', 'utf8'))

    def send_ping(self):
        ping = json.dumps({'msgtype': 'ping'})
        print("Pinging", self.remote_node_id)
        self.transport.write(bytes(ping + '\n', 'utf8'))

    def send_pong(self):
        pong = json.dumps({'msgtype': 'pong'})
        self.transport.write(bytes(pong + '\n', 'utf8'))

    def handle_ping(self):
        self.send_pong()

    def handle_pong(self):
        print("Got pong from", self.remote_node_id)
        self.last_ping = time()