import sys
from twisted.internet import endpoints, reactor

from p2p_factory import P2PFactory
from p2p_protocol import P2PProtocol

PORT = int(sys.argv[1])
BOOTSTRAP_LIST = sys.argv[2:]
print(BOOTSTRAP_LIST)

factory = P2PFactory(port=PORT)

# server
endpoint = endpoints.TCP4ServerEndpoint(reactor, int(PORT))
endpoint.listen(factory)

# client
for port in BOOTSTRAP_LIST:
    point = endpoints.TCP4ClientEndpoint(reactor, "localhost", int(port))
    d = endpoints.connectProtocol(point, P2PProtocol(factory=factory, peer_type=1))
reactor.run()