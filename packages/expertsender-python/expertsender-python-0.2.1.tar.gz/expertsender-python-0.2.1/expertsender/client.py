# -*- coding: utf-8 -*-
import requests

from .utils import xml2dict, generate_request_xml
from .errors import ExpertsenderError
from .suppression_lists import SuppressionListsMixin
from .email_messages import EmailMessagesMixin
from .subscribers import SubscriberMixin
from .export import ExportMixin


class ExpertsenderClient(SuppressionListsMixin, EmailMessagesMixin, SubscriberMixin, ExportMixin):
    def __init__(self, user: str, token: str, api_version: str = 'v2'):
        """
        Initialise the Expertsender client class
        :param user: The user is 'api', plus the server number the unit is one. E.g. 'api3'
        :param token: The API key
        """
        self.api_url = f'https://{user}.esv2.com/{api_version}/Api/'
        self.api_key = token

    def templates(self, t_type: str = None) -> dict:
        assert t_type in {'Header', 'Footer', None}, "Allowed Types are 'Header', 'Footer', and None."
        url = f'{self.api_url}Templates?apiKey={self.api_key}'
        if t_type:
            url = url + f"?type={t_type}"

        r_dict = self._es_get_request(url)
        templates = r_dict['ApiResponse']['Data']['Templates']
        if type(templates) == dict:
            return {templates['Template']['Id']: {'Name': templates['Template']['Name'],
                                                  'Type': templates['Template']['Type']}}
        else:
            return {t['Template']['Id']: {'Name': t['Template']['Name'], 'Type': t['Template']['Type']}
                    for t in templates}

    def custom_fields(self) -> dict:
        """
        Gets all custom fields created in the Unit
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/get-custom-fields-list
        :return: Dict with field name as key and id as value
        """
        url = f'{self.api_url}Fields?apiKey={self.api_key}'
        r_dict = self._es_get_request(url)
        self._check_response(r_dict)

        return {l['Field']['Name']: l['Field']['Id'] for l in
                r_dict['ApiResponse']['Data']['Fields']}  # list of dicts

    def _es_get_request(self, url: str) -> dict:
        # Takes in an url, checks the return for errors and returns the results as dict
        r = requests.get(url)
        r_dict = xml2dict(r.text)
        self._check_response(r_dict)

        return r_dict

    def _es_delete_request(self, url: str) -> dict:
        # Takes in an url, checks the return for errors and returns the results as dict
        r = requests.get(url)
        r_dict = xml2dict(r.text)
        self._check_response(r_dict)

        return r_dict

    def _es_post_request(self, url: str, data: dict = None, expect_return: bool = True) -> dict:
        # Takes in an url, checks the return for errors and returns the results as dict
        data = generate_request_xml(self.api_key, '', data)
        r = requests.post(url, data=data)
        if expect_return:
            r_dict = xml2dict(r.text)
            self._check_response(r_dict)

            return r_dict
        else:
            return_code = r.status_code
            first_digit = int(return_code / 100)
            if first_digit != 2:
                raise ExpertsenderError(r.content)
            else:
                return {}

    @staticmethod
    def _check_response(r_dict: dict):
        assert isinstance(r_dict, dict), "Input has to be a dict"
        if 'ErrorMessage' in r_dict['ApiResponse']:
            error_message = r_dict['ApiResponse']['ErrorMessage']
            raise ExpertsenderError(
                f"The request with error code {error_message['Code']}. "
                f"Error Message: {error_message['Message']}")
