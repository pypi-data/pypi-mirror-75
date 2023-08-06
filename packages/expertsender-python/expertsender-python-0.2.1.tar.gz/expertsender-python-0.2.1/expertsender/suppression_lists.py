from abc import ABC

from .utils import generate_request_xml


class SuppressionListsMixin(ABC):
    def create_suppression_list(self, name: str, list_type: str = 'Email', import_rule: str = 'Email'):
        """
        Create a Suppression list in that unit
        :param list_type: Email or SmsMms
        :param name: Name that the suppression is supposed to have
        :param import_rule: Either Email or EmailAndDomain
        :return:
        """
        data = generate_request_xml(self.api_key, '', {
            'Name': name,
            'Type': list_type,
            'ImportRule': import_rule
        })
        r_dict = self._es_post_request(f'{self.api_url}CreateSuppressionList', data)
        list_id = r_dict['ApiResponse']['Data']

        return list_id

    def suppression_lists(self) -> dict:
        """
        Gets all Suppression Lists created in the Unit
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/suppression-lists/get-suppression-lists
        :return: Nested dict with id as key and the list name as value
        """
        url = f'{self.api_url}SuppressionLists?apiKey={self.api_key}'
        r_dict = self._es_get_request(url)

        # Cover the case of only one suppression list
        suppression_lists = r_dict['ApiResponse']['Data']['SuppressionLists']

        if type(suppression_lists) == dict:
            return {suppression_lists['SuppressionList']['Id']: suppression_lists['SuppressionList']['Name']}
        else:
            # Returns segments as nested dict with id as key and the segment name and tags in the inner dict
            return {s['SuppressionList']['Id']: s['SuppressionList']['Name'] for s in suppression_lists}

    def add_to_suppression_list(self, email: str, list_id: int):
        """
        Add a user to a suppression list
        :param list_id: Expertsender Id of the suppression list
        :param email: User to be added
        """
        url = f'{self.api_url}SuppressionLists/{list_id}?apiKey={self.api_key}&entry={email}'
        _ = self._es_post_request(url)

    def remove_from_suppression_list(self, email: str, list_id: int):
        """
        Add a user to a suppression list
        :param list_id: Expertsender Id of the suppression list
        :param email: User to be added
        """
        url = f'{self.api_url}SuppressionLists/{list_id}?apiKey={self.api_key}&entry={email}'
        self._es_delete_request(url)
