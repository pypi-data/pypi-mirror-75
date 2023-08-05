import uuid

from securenative.context.context_builder import ContextBuilder
from securenative.models.request_context import RequestContextBuilder
from securenative.utils.date_utils import DateUtils
from securenative.utils.encryption_utils import EncryptionUtils


class SDKEvent(object):

    def __init__(self, event_options, securenative_options):
        if event_options.context is not None:
            self.context = event_options.context
        else:
            self.context = ContextBuilder.default_context_builder().build()

        client_token = EncryptionUtils.decrypt(self.context.client_token, securenative_options.api_key)

        self.rid = str(uuid.uuid4())
        self.event_type = event_options.event.value
        self.user_id = event_options.user_id
        self.user_traits = event_options.user_traits
        self.request = RequestContextBuilder() \
            .with_cid(client_token.cid if client_token else "") \
            .with_vid(client_token.vid if client_token else "") \
            .with_fp(client_token.fp if client_token else "") \
            .with_ip(self.context.ip) \
            .with_remote_ip(self.context.remote_ip) \
            .with_method(self.context.method) \
            .with_url(self.context.url) \
            .with_headers(self.context.headers) \
            .build()

        self.timestamp = DateUtils.to_timestamp(event_options.timestamp)
        self.properties = event_options.properties
