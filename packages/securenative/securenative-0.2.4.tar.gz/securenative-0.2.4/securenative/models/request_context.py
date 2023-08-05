class RequestContext(object):

    def __init__(self, cid=None, vid=None, fp=None, ip=None,
                 remote_ip=None, headers=None, url=None, method=None):
        self.cid = cid
        self.vid = vid
        self.fp = fp
        self.ip = ip
        self.remote_ip = remote_ip
        self.headers = headers
        self.url = url
        self.method = method


class RequestContextBuilder(object):

    def __init__(self, cid=None, vid=None, fp=None, ip=None,
                 remote_ip=None, headers=None, url=None, method=None):
        self.cid = cid
        self.vid = vid
        self.fp = fp
        self.ip = ip
        self.remote_ip = remote_ip
        self.headers = headers
        self.url = url
        self.method = method

    def with_cid(self, cid):
        self.cid = cid
        return self

    def with_vid(self, vid):
        self.vid = vid
        return self

    def with_fp(self, fp):
        self.fp = fp
        return self

    def with_ip(self, ip):
        self.ip = ip
        return self

    def with_remote_ip(self, remote_ip):
        self.remote_ip = remote_ip
        return self

    def with_headers(self, headers):
        self.headers = headers
        return self

    def with_url(self, url):
        self.url = url
        return self

    def with_method(self, method):
        self.method = method
        return self

    def build(self):
        return RequestContext(self.cid, self.vid, self.fp, self.ip, self.remote_ip, self.headers, self.url, self.method)
