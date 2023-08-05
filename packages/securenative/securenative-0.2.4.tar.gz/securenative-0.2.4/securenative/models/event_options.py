class EventOptions(object):

    def __init__(self, event, user_id=None, user_traits=None,
                 context=None, properties=None, timestamp=None):
        self.event = event
        self.user_id = user_id
        self.user_traits = user_traits
        self.context = context
        self.properties = properties
        self.timestamp = timestamp
