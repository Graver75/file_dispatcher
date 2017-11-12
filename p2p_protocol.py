from twisted.internet.protocol import Protocol


class P2PProtocol(Protocol):
    def __init__(self):
        self.state = "HELLO"
        self.remote_node_id = None

