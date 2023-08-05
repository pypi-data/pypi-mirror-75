from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException
from securenative.models.event_options import EventOptions
from securenative.models.user_traits import UserTraits


class EventOptionsBuilder(object):
    MAX_PROPERTIES_SIZE = 10

    def __init__(self, event_type):
        self.event_options = EventOptions(event_type)

    def with_user_id(self, user_id):
        self.event_options.user_id = user_id
        return self

    def with_user_traits(self, user_traits):
        self.event_options.user_traits = user_traits
        return self

    def with_user(self, name, email, phone=None, created_at=None):
        self.event_options.user_traits = UserTraits(name, email, phone, created_at)
        return self

    def with_context(self, context):
        self.event_options.context = context
        return self

    def with_properties(self, properties):
        self.event_options.properties = properties
        return self

    def with_timestamp(self, timestamp):
        self.event_options.timestamp = timestamp
        return self

    def build(self):
        if self.event_options.properties is not None \
                and len(self.event_options.properties) > self.MAX_PROPERTIES_SIZE:
            raise SecureNativeInvalidOptionsException(
                "You can have only up to {} custom properties", self.MAX_PROPERTIES_SIZE)
        return self.event_options
