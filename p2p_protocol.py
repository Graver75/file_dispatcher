from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor
from time import time
import json

from helper import Helper

RECOVERY_DELAY = 120
PING_INTERVAL = min(RECOVERY_DELAY, 5)
GETADDR_INTERVAL = 10
GETFILENAMES_INTERVAL = 30


class P2PProtocol(Protocol):
    """
    Peer type 0 means that we have a connection from him
    Peer type 1 means that we try to connect to him
    """

    def __init__(self, factory, peer_type=0):
        self.factory = factory
        self.state = "HELLO"
        self.remote_node_id = None
        self.remote_file_names = []
        self.lc_ping = LoopingCall(self.send_ping)
        self.lc_addr = LoopingCall(self.send_getaddr)
        self.lc_filenames = LoopingCall(self.send_getfilenames)
        self.last_ping = 0
        self.peer_type = peer_type

    def connectionMade(self):
        print('Connection made from', self.transport.getPeer())
        self.last_ping = time()
        self.send_hello()

    # TODO: fix reason
    def connectionLost(self, reason=True):
        if self.remote_node_id in self.factory.peers:
            self.factory.peers.pop(self.remote_node_id)
            self.lc_ping.stop()
            self.lc_addr.stop()
        print(self.remote_node_id, ': disconnected')

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
            elif msg_type == "getaddr":
                self.handle_getaddr()
            elif msg_type == "addr":
                self.handle_addr(line)
            elif msg_type == "getfilenames":
                self.handle_getfilenames()
            elif msg_type == "filenames":
                self.handle_filenames(line)

    def handle_addr(self, addr):
        addr = json.loads(addr)
        for remote_ip, remote_node_id in addr['peers']:
            if remote_node_id not in self.factory.peers:
                host, port = remote_ip.split(":")
                point = TCP4ClientEndpoint(reactor, host, int(port))
                d = connectProtocol(point, P2PProtocol(factory=self.factory))

    def handle_hello(self, hello):
        hello = json.loads(hello)
        self.remote_node_id = hello["node_id"]
        if self.remote_node_id == self.factory.node_id:
            print('Connection loop')
            self.transport.loseConnection()
        else:
            print(self.remote_node_id, ': hello')
            self.factory.peers[self.remote_node_id] = self
            self.remote_ip = hello['ip'] + ':' + str(hello['port'])
            self.lc_ping.start(PING_INTERVAL)
            self.lc_addr.start(GETADDR_INTERVAL)
            self.lc_filenames.start(GETFILENAMES_INTERVAL)
            self.send_addr(mine=True)
            self.send_getfilenames()

    def send_hello(self):
        self.transport.write(Helper.presend({'node_id': self.factory.node_id,
                                             'msgtype': 'hello',
                                             'ip': self.factory.ip,
                                             'port': self.factory.port
                                             }))

    def send_ping(self):
        if not self.is_dead_node(self):
            print(self.remote_node_id, ": ping")
            self.transport.write(Helper.presend({'msgtype': 'ping'}))
        else:
            self.transport.loseConnection()

    def send_pong(self):
        self.transport.write(Helper.presend({'msgtype': 'pong'}))

    def handle_ping(self):
        self.send_pong()

    def handle_pong(self):
        print(self.remote_node_id, ": pong")
        self.last_ping = time()

    @staticmethod
    def is_dead_node(node):
        return (time() - node.last_ping) > RECOVERY_DELAY

    def handle_getaddr(self):
        self.send_addr()

    def send_addr(self, mine=False):
        if mine:
            peers = [(self.factory.ip + ":" + str(self.factory.port), self.factory.node_id)]
        else:
            peers = [(self.factory.peers[peer].remote_ip, self.factory.peers[peer].remote_node_id)
                     for peer in self.factory.peers
                     if self.factory.peers[peer].peer_type == 0 and
                     not self.is_dead_node(self.factory.peers[peer])]
        self.transport.write(Helper.presend({"msgtype": "addr", "peers": peers}))

    def send_getaddr(self):
        self.transport.write(Helper.presend({"msgtype": "getaddr"}))

    def send_getfilenames(self):
        self.transport.write(Helper.presend({"msgtype": "getfilenames"}))

    def handle_getfilenames(self):
        self.send_file_names()

    def send_file_names(self):
        self.transport.write(Helper.presend({"msgtype": "filenames", "filenames": self.factory.file_names}))

    def handle_filenames(self, filenames):
        filenames = json.loads(filenames)
        for file_name in filenames:
            if file_name not in self.factory.peers[self.remote_node_id].remote_file_names:
                self.factory.peers[self.remote_node_id].remote_file_names.append(file_name)