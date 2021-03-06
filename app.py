from twisted.internet import endpoints, reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB

from p2p_factory import P2PFactory
from p2p_protocol import P2PProtocol
from config import PORT, FILE_DIRECTORY, BOOTSTRAP_LIST, WANNA_CONTROL_SERVER


factory = P2PFactory(port=PORT)

# ftp
p = Portal(FTPRealm(FILE_DIRECTORY),
           [AllowAnonymousAccess(), FilePasswordDB("./pass.dat")])
f = FTPFactory(p)
reactor.listenTCP(9021, f)

# server
endpoint = endpoints.TCP4ServerEndpoint(reactor, PORT)
endpoint.listen(factory)

# client
for address in BOOTSTRAP_LIST:
    host, port = address.split(':')
    point = endpoints.TCP4ClientEndpoint(reactor, host, int(port))
    d = endpoints.connectProtocol(point, P2PProtocol(factory=factory, peer_type=1))
if WANNA_CONTROL_SERVER:
    from http_control_server import HTTPControlServer
    HTTPControlServer(factory).app.run('localhost', 8080)
reactor.run()
