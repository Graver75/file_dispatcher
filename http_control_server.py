import json

from helper import Helper

from klein import Klein
from twisted.web.static import File


class HTTPControlServer:
    app = Klein()
    
    def __init__(self, factory):
        self._factory = factory
    
    @app.route('/', branch=True)
    def static(self, request):
        return File("./web/static")

    @app.route('/api/info')
    def send_info(self, request):
        return Helper.presend({
            "id": self._factory.node_id,
            "ip": self._factory.ip,
            "port": self._factory.port
        })

    @app.route('/api/nodes')
    def send_nodes(self, request):
        return Helper.presend(([(node.remote_ip, node.remote_node_id) for node in self._factory.peers]))
