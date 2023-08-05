import json
import unittest
import responses

from securenative.api_manager import ApiManager
from securenative.config.configuration_manager import ConfigurationManager
from securenative.context.context_builder import ContextBuilder
from securenative.enums.event_types import EventTypes
from securenative.enums.risk_level import RiskLevel
from securenative.event_manager import EventManager
from securenative.event_options_builder import EventOptionsBuilder
from securenative.exceptions.securenative_invalid_options_exception import SecureNativeInvalidOptionsException
from securenative.models.user_traits import UserTraits
from securenative.models.verify_result import VerifyResult


class ApiManagerTest(unittest.TestCase):

    def setUp(self):
        self.context = ContextBuilder(). \
            with_ip("127.0.0.1"). \
            with_headers(
            {
                "user-agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
            }).build()

        self.event_options = EventOptionsBuilder(EventTypes.LOG_IN). \
            with_user_id("USER_ID"). \
            with_user_traits(UserTraits("USER_NAME", "USER_EMAIL", "+12012673412")). \
            with_context(self.context). \
            with_properties({"prop1": "CUSTOM_PARAM_VALUE",
                             "prop2": True,
                             "prop3": 3}).build()

    @responses.activate
    def test_track_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10). \
            with_api_url("https://api.securenative-stg.com/collector/api/v1")

        expected = "{\"eventType\":\"sn.user.login\",\"userId\":\"USER_ID\",\"userTraits\":{" \
                   "\"name\":\"USER_NAME\",\"email\":\"USER_EMAIL\",\"createdAt\":null},\"request\":{" \
                   "\"cid\":null,\"vid\":null,\"fp\":null,\"ip\":\"127.0.0.1\",\"remoteIp\":null,\"headers\":{" \
                   "\"user-agent\":\"Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) " \
                   "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405\"},\"url\":null,\"method\":null}," \
                   "\"properties\":{\"prop2\":true,\"prop1\":\"CUSTOM_PARAM_VALUE\",\"prop3\":3}}"

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/track",
                      json=json.loads(expected), status=200)
        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            api_manager.track(self.event_options)
        finally:
            event_manager.stop_event_persist()

    @responses.activate
    def test_securenative_invalid_options_exception(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_auto_send(True). \
            with_interval(10). \
            with_api_url("https://api.securenative-stg.com/collector/api/v1")

        properties = {}
        for i in range(1, 12):
            properties[i] = i

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/track",
                      json={}, status=200)
        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        try:
            with self.assertRaises(SecureNativeInvalidOptionsException):
                api_manager.track(EventOptionsBuilder(
                    EventTypes.LOG_IN).with_properties(properties).build())
        finally:
            event_manager.stop_event_persist()

    @responses.activate
    def test_verify_event(self):
        options = ConfigurationManager.config_builder(). \
            with_api_key("YOUR_API_KEY"). \
            with_api_url("https://api.securenative-stg.com/collector/api/v1")

        responses.add(responses.POST, "https://api.securenative-stg.com/collector/api/v1/verify",
                      json={
                          "riskLevel": "low",
                          "score": 0,
                          "triggers": None
                      }, status=200)
        verify_result = VerifyResult(RiskLevel.LOW, 0, None)

        event_manager = EventManager(options)
        event_manager.start_event_persist()
        api_manager = ApiManager(event_manager, options)

        result = api_manager.verify(self.event_options)

        self.assertIsNotNone(result)
        self.assertEqual(result.risk_level, verify_result.risk_level.value)
        self.assertEqual(result.score, verify_result.score)
        self.assertEqual(result.triggers, verify_result.triggers)


if __name__ == '__main__':
    unittest.main()
