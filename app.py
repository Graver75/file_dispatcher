import sys
from twisted.internet import endpoints, reactor

from p2p_factory import P2PFactory
from p2p_protocol import P2PProtocol

# server
endpoint = endpoints.TCP4ServerEndpoint(reactor, int(sys.argv[1]))
endpoint.listen(P2PFactory())

# client
point = endpoints.TCP4ClientEndpoint(reactor, "localhost", int(sys.argv[1]))
d = endpoints.connectProtocol(point, P2PProtocol(factory=P2PFactory))
reactor.run()