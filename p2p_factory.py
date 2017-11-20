from twisted.internet.protocol import Factory

from p2p_protocol import P2PProtocol
from helper import Helper


class P2PFactory(Factory):
    protocol = P2PProtocol

    def __init__(self, port):
        self.port = port

    def startFactory(self):
        self.node_id = Helper.generate_node_id()
        self.peers = {}
        print('Factory: started')

    def stopFactory(self):
        print('Factory: stopped')

    def buildProtocol(self, addr):
        return P2PProtocol(self)
