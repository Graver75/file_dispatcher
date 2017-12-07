import json
import re

from helper import Helper

from flask import Flask, send_from_directory
from klein import Klein
from twisted.web.static import File


class HTTPControlServer:
    #app = Flask(__name__, static_url_path='')
    app = Klein()
    
    def __init__(self, factory):
        self._factory = factory
    
    #@app.route('/<path:path>')
    @app.route('/', branch=True)
    def static(self, path):
        #return send_from_directory("./web/static", path)
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
    def send_filenames(self, request):
        return Helper.presend(self._factory.file_names)

    #with app.subroute('/api/nodes') as app:
    #    @app.route(re.compile('/'))
    #   def get_files(self, request):
    #        pass