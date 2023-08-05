# coding: utf-8
import os
import unittest
import json
from mock import Mock, patch

from otrs_somconnexio.exceptions import ErrorSettingPreference
from otrs_somconnexio.user_management_client.client import UserManagementClient

USER = 'user'
PASSW = 'passw'
URL = 'https://otrs-url.coop/'


@patch.dict(os.environ, {
    'OTRS_USER': USER,
    'OTRS_PASSW': PASSW,
    'OTRS_URL': URL
})
class UserManagementClientTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.user_management_client.client.requests', spec=['post'])
    def test_set_user_preference(self, requests_mock):
        user_id = 'test@test.test'
        lang = 'es'
        preference_key = 'UserLanguage'

        expected_url = '{}otrs/nph-genericinterface.pl/Webservice/UserManagement/cuser'.format(URL)
        expected_body = {
            "UserLogin": USER,
            "Password": PASSW,
            "Object": "Kernel::System::CustomerUser",
            "Method": "SetPreferences",
            "Parameter": {
                "Key": preference_key,
                "Value": lang,
                "UserID": user_id
            }
        }
        requests_mock.post.return_value = Mock(spec=['json'])
        requests_mock.post.return_value.json.return_value = {"Result": [1]}

        UserManagementClient().set_preference(preference_key, user_id, lang)

        requests_mock.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))

    @patch('otrs_somconnexio.user_management_client.client.requests', spec=['post'])
    def test_set_user_preference_raise_error_if_fails(self, requests_mock):
        user_id = 'test@test.test'
        lang = 'es'
        preference_key = 'UserLanguage'

        requests_mock.post.return_value = Mock(spec=['json'])
        requests_mock.post.return_value.json.return_value = {"Result": []}

        with self.assertRaises(ErrorSettingPreference):
            UserManagementClient().set_preference(preference_key, user_id, lang)
