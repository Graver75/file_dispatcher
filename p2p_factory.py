from twisted.internet.protocol import Factory

from p2p_protocol import P2PProtocol
from helper import Helper


class P2PFactory(Factory):
    protocol = P2PProtocol

    def startFactory(self):
        self.node_id = Helper.generate_node_id()
        self.peers = {}
