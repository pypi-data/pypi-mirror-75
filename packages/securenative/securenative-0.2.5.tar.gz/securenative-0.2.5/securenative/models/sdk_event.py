import uuid

from securenative.context.context_builder import ContextBuilder
from securenative.models.request_context import RequestContextBuilder
from securenative.models.user_traits import UserTraits
from securenative.utils.date_utils import DateUtils
from securenative.utils.encryption_utils import EncryptionUtils


class SDKEvent(object):

    def __init__(self, event_options, securenative_options):
        if event_options.context is not None:
            self.context = event_options.context
        else:
            self.context = ContextBuilder.default_context_builder().build()

        if self.context.client_token:
            client_token = EncryptionUtils.decrypt(self.context.client_token, securenative_options.api_key)
        else:
            client_token = None

        if event_options.user_traits and isinstance(event_options.user_traits, dict):
            user_traits = UserTraits(event_options.user_traits.get("name", ""),
                                     event_options.user_traits.get("email", ""),
                                     event_options.user_traits.get("phone", ""),
                                     event_options.user_traits.get("created_at", ""))
        elif event_options.user_traits:
            user_traits = event_options.user_traits
        else:
            user_traits = UserTraits()

        self.rid = str(uuid.uuid4())
        self.event_type = event_options.event if event_options.event else ""
        self.user_id = event_options.user_id if event_options.user_id else ""
        self.user_traits = user_traits
        self.request = RequestContextBuilder() \
            .with_cid(client_token.cid if client_token else "") \
            .with_vid(client_token.vid if client_token else "") \
            .with_fp(client_token.fp if client_token else "") \
            .with_ip(self.context.ip if self.context.ip else "") \
            .with_remote_ip(self.context.remote_ip if self.context.remote_ip else "") \
            .with_method(self.context.method if self.context.method else "") \
            .with_url(self.context.url if self.context.url else "") \
            .with_headers(self.context.headers if self.context.headers else None) \
            .build()

        self.timestamp = DateUtils.to_timestamp(event_options.timestamp)
        self.properties = event_options.properties
