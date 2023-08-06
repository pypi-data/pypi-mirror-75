from abc import ABC


class SubscriberMixin(ABC):
    def lists(self, seed_lists=False) -> dict:
        """
        Gets all Segments created in the Unit
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/get-subscriber-lists
        :return: Dict of lists with list-id as key and list name as value
        """
        url = f'{self.api_url}Lists?apiKey={self.api_key}&seedLists={seed_lists}'

        r_dict = self._es_get_request(url)
        lists = r_dict['ApiResponse']['Data']['Lists']

        # Returns lists as dict with id as key and name as value, this order because id is unique
        if type(lists) == dict:
            return {lists['List']['Id']: lists['List']['Name']}
        else:
            return {l['List']['Id']: l['List']['Name'] for l in lists}

    def segments(self) -> dict:
        """
        Gets all Segments created in the Unit
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/get-subscriber-segments
        :return: Nested dict with id as key and the segment name and tags in the inner dict
        """
        url = f'{self.api_url}Segments?apiKey={self.api_key}'
        r_dict = self._es_get_request(url)
        segments = r_dict['ApiResponse']['Data']['Segments']

        for s in segments:
            # If no Tags, the value will be an empty string
            if type(s['Segment']['Tags']) == str:
                s['Segment']['Tags'] = []
            # If only one tag, the value will be a dictionary
            elif type(s['Segment']['Tags']) == dict:
                s['Segment']['Tags'] = [s['Segment']['Tags']]

        # Returns lists as dict with id as key and name as value, this order because id is unique
        if type(segments) == dict:
            return {segments['Segment']['Id']: {'Name': segments['Segment']['Name'],
                                                'Tags': [tag['Tag'] for tag in segments['Segment']['Tags']]}}
        else:
            return {
                s['Segment']['Id']: {'Name': s['Segment']['Name'], 'Tags': [tag['Tag'] for tag in s['Segment']['Tags']]}
                for s in r_dict['ApiResponse']['Data']['Segments']}

    def create_list(self, list_name, is_seed_list=False):
        """
        Creates a seed list with the name 'api_subscribers', which is used for sending test emails
        :return: The list id of the created seed-list
        """
        data = {
            'GeneralSettings': dict(Name=list_name,
                                    IsSeedList=is_seed_list)
        }
        r_dict = self._es_post_request(f'{self.api_url}Lists', data)
        # Return the id of the newly created list
        return r_dict['ApiResponse']['Data']

    def add_subscriber(self, list_id: str, email: str):
        """
        Add a subscriber to any list (seed or regular list)
        :param list_id:
        :param email:
        """
        data = {
            'ListId': list_id,
            'Email': email
        }
        _ = self._es_post_request(f'{self.api_url}Subscribers', data, expect_return=False)
