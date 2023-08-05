from securenative.context.securenative_context import SecureNativeContext
from securenative.utils.request_utils import RequestUtils
from securenative.utils.utils import Utils


class ContextBuilder(object):

    def __init__(self):
        self.context = SecureNativeContext()

    def with_client_token(self, client_token):
        self.context.client_token = client_token
        return self

    def with_ip(self, ip):
        self.context.ip = ip
        return self

    def with_remote_ip(self, remote_ip):
        self.context.remote_ip = remote_ip
        return self

    def with_headers(self, headers):
        self.context.headers = headers
        return self

    def with_url(self, url):
        self.context.url = url
        return self

    def with_method(self, method):
        self.context.method = method
        return self

    def with_body(self, body):
        self.context.body = body
        return self

    @staticmethod
    def default_context_builder():
        return ContextBuilder()

    @staticmethod
    def from_http_request(request):
        try:
            client_token = request.cookies[RequestUtils.SECURENATIVE_COOKIE]
        except AttributeError:
            client_token = None

        try:
            headers = request.headers
        except AttributeError:
            headers = None

        if Utils.is_null_or_empty(client_token):
            client_token = RequestUtils.get_secure_header_from_request(headers)

        return ContextBuilder()\
            .with_url(request.url)\
            .with_method(request.method)\
            .with_headers(headers)\
            .with_client_token(client_token)\
            .with_ip(RequestUtils.get_client_ip_from_request(request))\
            .with_remote_ip(RequestUtils.get_remote_ip_from_request(request))\
            .with_body(None)

    def build(self):
        return self.context
