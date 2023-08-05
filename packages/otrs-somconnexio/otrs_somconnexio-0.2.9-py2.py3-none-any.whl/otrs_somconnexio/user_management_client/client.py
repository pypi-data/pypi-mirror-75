import requests
import os
import json

from otrs_somconnexio.exceptions import ErrorSettingPreference


class UserManagementClient:
    WEBSERVICES_PATH = 'otrs/nph-genericinterface.pl/Webservice/UserManagement/cuser'

    @staticmethod
    def _password():
        return os.environ['OTRS_PASSW']

    @staticmethod
    def _user():
        return os.environ['OTRS_USER']

    @staticmethod
    def _url():
        return os.environ['OTRS_URL']

    @classmethod
    def set_preference(cls, key, user_id, lang):
        payload = {
            "UserLogin": cls._user(),
            "Password": cls._password(),
            "Object": "Kernel::System::CustomerUser",
            "Method": "SetPreferences",
            "Parameter": {
                "Key": key,
                "Value": lang,
                "UserID": user_id
            }
        }
        json_payload = json.dumps(payload)
        url = '{}{}'.format(cls._url(), cls.WEBSERVICES_PATH)
        response = requests.post(url, data=json_payload)

        # TODO: We ask to change the behaviour of this endpoint.
        # Raise an error and return a status 200 it's not a good idea.
        if response.json()['Result'] == []:
            raise ErrorSettingPreference(
                "Error setting the language code {} to user {}".format(lang, user_id)
            )
