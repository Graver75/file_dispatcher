from twisted.protocols.ftp import FTPClient
from twisted.internet.protocol import ClientCreator
from twisted.internet import reactor



def fail(error):
    print('Failed.  Error was:')
    print(error)

def get_buffer_value(result, bufferProtocol):
    return bufferProtocol.buffer.getvalue()

def run(opts, callback):
    # Create the client
    FTPClient.debug = 1
    creator = ClientCreator(reactor, FTPClient, 'anonymous',
                            'twisted@', passive=0)
    creator.connectTCP(opts['host'], opts['port']).addCallback(callback).addErrback(
        connectionFailed)


def connectionFailed(f):
    print("Connection Failed:", f)
