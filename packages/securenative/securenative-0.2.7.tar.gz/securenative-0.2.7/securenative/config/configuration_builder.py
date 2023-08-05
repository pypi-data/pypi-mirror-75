from securenative.config.securenative_options import SecureNativeOptions
from securenative.enums.failover_strategy import FailOverStrategy


class ConfigurationBuilder(object):

    def __init__(self):
        self.api_key = None
        self.api_url = "https://api.securenative.com/collector/api/v1"
        self.interval = 1000
        self.max_events = 1000
        self.timeout = 1500
        self.auto_send = True
        self.disable = False
        self.log_level = "CRITICAL"
        self.fail_over_strategy = FailOverStrategy.FAIL_OPEN.value

    @staticmethod
    def default_config_builder():
        return ConfigurationBuilder()

    def with_api_key(self, api_key):
        self.api_key = api_key
        return self

    def with_api_url(self, api_url):
        self.api_url = api_url
        return self

    def with_interval(self, interval):
        self.interval = interval
        return self

    def with_max_events(self, max_events):
        self.max_events = max_events
        return self

    def with_timeout(self, timeout):
        self.timeout = timeout
        return self

    def with_auto_send(self, auto_send):
        self.auto_send = auto_send
        return self

    def with_disable(self, disable):
        self.disable = disable
        return self

    def with_log_level(self, log_level):
        self.log_level = log_level
        return self

    def with_fail_over_strategy(self, fail_over_strategy):
        if fail_over_strategy != FailOverStrategy.FAIL_OPEN.value and \
                fail_over_strategy != FailOverStrategy.FAIL_CLOSED.value:
            self.fail_over_strategy = FailOverStrategy.FAIL_OPEN.value
            return self
        self.fail_over_strategy = fail_over_strategy
        return self

    def build(self):
        return self

    @staticmethod
    def get_default_securenative_options():
        return SecureNativeOptions()
