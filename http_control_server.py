from helper import Helper

from klein import Klein
from twisted.web.static import File


class HTTPControlServer:
    app = Klein()
    
    def __init__(self, factory):
        self._factory = factory
    
    @app.route('/', branch=True)
    def static(self, path):
        return File('./web/static')

    @app.route('/api/info')
    def send_info(self, request):
        return Helper.presend({
            "id": self._factory.node_id,
            "ip": self._factory.ip,
            "port": self._factory.port
        })

    @app.route('/api/nodes')
    def send_nodes(self, request):
        return Helper.presend({node: self._factory.peers[node].remote_ip for node in self._factory.peers})

    @app.route('/api/files')
    def send_own_filenames(self, request):
        return Helper.presend(self._factory.file_names)

    @app.route('/api/nodes/<string:id>/files')
    def send_filenames(self, request, id):
        return Helper.presend(self._factory.peers[id].remote_file_names)

    @app.route('/api/nodes/<string:id>/files/<string:name>')
    def fetch_file(self, request, id, name):
        Helper.retrieve_file_from_ftp(name, self._factory.peers[id].remote_ftp_client)
        return request.setResponseCode(200)
