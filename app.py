from twisted.internet import endpoints, reactor

from p2p_factory import P2PFactory
from p2p_protocol import P2PProtocol

# server
endpoint = endpoints.TCP4ServerEndpoint(reactor, 7003)
endpoint.listen(P2PFactory())

# client
point = endpoints.TCP4ClientEndpoint(reactor, "localhost", 7003)
d = endpoints.connectProtocol(point, P2PProtocol(factory=P2PFactory))
reactor.run()