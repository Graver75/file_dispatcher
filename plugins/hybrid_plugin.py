def extend_klein_server(server, apis):
    for api in apis:
        @server.app.route(api.url)
        def api_method(*args, **kwargs):
            caller = api.handler
            caller(**locals())
