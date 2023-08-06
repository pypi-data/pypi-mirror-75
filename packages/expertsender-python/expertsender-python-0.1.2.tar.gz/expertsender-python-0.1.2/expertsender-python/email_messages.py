from datetime import datetime


class EmailMessagesMixin:
    def create_transactional(self, from_email: str, from_name: str, subject: str, reply_name: str = None,
                             html: str = None, plain: str = None, header: str = None, footer: str = None,
                             tags: list = None, channels: dict = None):
        """
        In Expertsender, Mailings can only be send to a list of email addresses, if it was setup as an transactional
        mailing first.
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/messages/create-transactional-messages
        :param reply_name: String put into “Reply-To:” header. Optional.
        :param from_email: Email put into “From:” header. Required.
        :param channels: Dictionary of channels (IPs), key is the ip address, value is the percentage (needs to add up
            to 100). Optional.
        :param footer: ID of footer template to use. Optional.
        :param header: ID of header template to use. Optional.
        :param plain: Plain text content of transactional. Optional.
        :param html: HTML content of transactional. Optional.
        :param subject: Transactional's subject. Required.
        :param from_name: String put into “From:” header. Required.
        :param tags: List of tags used to mark the transactional for convenience reasons. Optional.
        :return: Expertsender ID of the created mailing
        """
        headers = {'Content-Type': 'text/xml;charset=UTF-8'}
        data_dict = {
            'Content': dict(FromName=from_name,
                            FromEmail=from_email,
                            ReplyName=reply_name,
                            Subject=subject,
                            Html=html,
                            Plain=plain,
                            Header=header,
                            Footer=footer,
                            Tags=[{'Tag': tag} for tag in tags])
        }

        # If the Mailing is
        if channels:
            data_dict.update({
                'Channels': [
                    {'Channel': dict(Ip=k, Percentage=v)} for k, v in channels.items()
                ]
            })

        r_dict = self._es_post_request(f'{self.api_url}TransactionalsCreate', data_dict)

        transactional_id = r_dict['ApiResponse']['Data']

        return transactional_id

    def create_send_newsletter(self, from_email: str, from_name: str, subject: str, reply_name: str = None,
                               html: str = None, plain: str = None, header: str = None, footer: str = None,
                               tags: list = None, channels: dict = None, lists: list = None, segments: list = None,
                               seed_lists: list = None, suppression_lists: list = None, throttling: str = 'Auto',
                               delivery_date: datetime = None):
        """
        In Expertsender, Mailings can only be send to a list of email addresses, if it was setup as an transactional
        mailing first.
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/messages/create-transactional-messages
        :param throttling: Delivery throttling method. See below for description of different throttling methods.
            Optional. Default is "Auto".
        :param delivery_date: Newsletter delivery date. Optional. By default, newsletter will be sent immediately.
        :param suppression_lists: List of SuppressionList elements containing IDs od suppression lists that will be
            checked during shipment. Optional.
        :param seed_lists: List of SeedList elements containing IDs of seed lists used during shipment. Optional.
        :param segments: List of SubscriberSegment elements containing IDs of subscriber segments that newsletter will
            be sent to. Optional.
        :param lists: List of SubscriberList elements containing IDs of subscriber lists that newsletter will be
            sent to. Optional.
        :param reply_name: String put into “Reply-To:” header. Optional.
        :param from_email: Email put into “From:” header. Required.
        :param channels: Dictionary of channels (IPs), key is the ip address, value is the percentage (needs to add up
            to 100). Optional.
        :param footer: ID of footer template to use. Optional.
        :param header: ID of header template to use. Optional.
        :param plain: Plain text content of transactional. Optional.
        :param html: HTML content of transactional. Optional.
        :param subject: Transactional's subject. Required.
        :param from_name: String put into “From:” header. Required.
        :param tags: List of tags used to mark the transactional for convenience reasons. Optional.
        :return: Expertsender ID of the created mailing
        """
        assert throttling in {'None', 'Auto', 'TimeOptimized', 'TimeTravel'}, "Throttling method not valid."
        headers = {'Content-Type': 'text/xml;charset=UTF-8'}

        data_dict = {
            'Recipients': dict(SubscriberLists=[{'SubscriberList': l} for l in lists or {}],
                               SubscriberSegments=[{'SubscriberSegment': s} for s in segments or {}],
                               SeedLists=[{'SeedList': sl} for sl in seed_lists or {}],
                               SuppressionLists=[{'SuppressionList': sl} for sl in suppression_lists or {}]),
            'Content': dict(FromName=from_name,
                            FromEmail=from_email,
                            ReplyName=reply_name,
                            Subject=subject,
                            Html=html,
                            Plain=plain,
                            Header=header,
                            Footer=footer,
                            Tags=[{'Tag': tag} for tag in tags or {}]),
            'DeliverySettings': dict(Channels=[{'Channel': dict(Ip=k, Percentage=v)}
                                               for k, v in channels.items() or {}],
                                     DeliveryDate=delivery_date.strftime('%Y-%m-%dT%H:%M:%S'),
                                     ThrottlingMethod=throttling),
        }

        r_dict = self._es_post_request(f'{self.api_url}Newsletters', data_dict)
        transactional_id = r_dict['ApiResponse']['Data']

        return transactional_id
