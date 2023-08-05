from flask import Flask, request, g

from skywalking import config, agent, Layer, Component
from skywalking.trace import tags
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import Tag


class SkywalkingFlask(object):
    def __init__(self, app: Flask,
                 service: str = None,
                 instance: str = None,
                 collector: str = None,
                 protocol_type: str = 'grpc',
                 token: str = None):
        self._app = app
        config.init(service, instance, collector, protocol_type, token)
        agent.start()

        if self._app:
            @app.before_request
            def before_request_tracing():
                if agent.connected():
                    carrier = Carrier()
                    for item in carrier:
                        item.val = request.headers.get(item.key.capitalize(), None)
                    context = get_context()
                    span = context.new_entry_span(op=request.path, carrier=carrier)
                    span.start()
                    span.layer = Layer.Http
                    span.component = Component.General
                    span.peer = str(request.host)
                    span.tag(Tag(key=tags.HttpMethod, val=request.method))
                    g.span = span

            @app.after_request
            def after_request_tracing(response):
                if agent.connected():
                    if hasattr(g, "span") and g.span:
                        span = g.span
                        span.tag(Tag(key=tags.HttpUrl, val=str(request.url)))
                        span.tag(Tag(key=tags.HttpStatus, val=response.status_code))
                        span.stop()
                return response

            @app.errorhandler(Exception)
            def exception_tracing(e):
                if agent.connected():
                    if hasattr(g, "span") and g.span:
                        span = g.span
                        span.raised()
                return e
