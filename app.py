from twisted.internet import endpoints, reactor

from p2p_factory import P2PFactory

fingerEndpoint = endpoints.serverFromString(reactor, "tcp:3007")
fingerEndpoint.listen(P2PFactory())
reactor.run()