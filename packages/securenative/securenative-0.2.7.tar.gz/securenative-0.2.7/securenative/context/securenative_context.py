class SecureNativeContext(object):

    def __init__(self, client_token=None, ip=None, remote_ip=None, headers=None, url=None, method=None, body=None):
        self.client_token = client_token
        self.ip = ip
        self.remote_ip = remote_ip
        self.headers = headers
        self.url = url
        self.method = method
        self.body = body
