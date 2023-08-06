from abc import ABC
from datetime import date
import uuid  # For generating random file names

from loguru import logger
import paramiko
import requests
try:
    import pandas as pd
except ImportError:
    pd = None

from .client import ExpertsenderClient
from .errors import ExpertsenderImportError


class ExpertsenderImporter:
    """
    Implements all functions regarding the mass-import of subscribers into Expertsender.
    These functions require Pandas to be installed (optional dependency.)
    """
    def __init__(self, client: ExpertsenderClient, sftp_host: str, sftp_user: str, sftp_pw):
        self.client = client
        self.sftp_host = sftp_host
        self.sftp_user = sftp_user
        self.sftp_pw = sftp_pw
        self._create_sftp_con()

    def _create_sftp_con(self):
        # Only sFTP is supported, so port is always 22
        transport = paramiko.Transport((self.sftp_host, 22))
        # Authentication and creating the sFTP Client
        transport.connect(None, self.sftp_user, self.sftp_pw)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def _upload_to_sftp(self, df: pd.DataFrame) -> str:
        """
        Writes a DataFrame to an sFTP server
        :param df: DataFrame containing the data to be saved
        :return: Uri of the file on the server
        """
        today = date.today().strftime('%Y%m%d')
        file_path = f'es_upload/{today}_{uuid.uuid4()}.csv'
        with self.sftp.open(file_path, 'w') as f:
            f.write(df.to_csv(index=False))

        return f'{self.sftp_host}/{file_path}'

    def _remove_from_sftp(self, file_path) -> bool:
        """

        :param file_path:
        :return: Returns True or raises an error
        """
        self.sftp.remove(file_path)
        return True

    def import_data(self, df: pd.DataFrame, list_id: str, cols: list = 'all', import_name: str = 'API Import',
                    import_mode: str = 'AddAndUpdate', allow_import_unsubscribed: bool = False,
                    allow_import_removed: bool = False):
        assert str(
            list_id) in self.client.lists(), f"The list_id {list_id} does not exists in the chosen Expertsender Unit."

        if type(cols) == list:
            df = df[cols].copy()

        system_fields = [
            'Id', 'FirstName', 'LastName', 'Email', 'EmailMd5', 'EmailSha256',
            'CustomSubscriberId', 'IP', 'Vendor', 'TrackingCode', 'GeoCountry',
            'GeoState', 'GeoCity', 'GeoZipCode', 'LastActivity', 'LastMessage',
            'LastEmail', 'LastOpenEmail', 'LastClickEmail', 'SubscriptionDate'
        ]
        custom_fields = self.client.custom_fields()

        # Make sure that all fields in the DataFrame have an equivalent in Expertsender
        assert df.columns.isin(system_fields + list(custom_fields.keys())).all(), \
            "All DataFrame columns need to exist either as Expertsender system field, or as custom field."

        logger.info("Starting upload of DataFrame to sFTP Server.")
        file_url = self._upload_to_sftp(df)
        logger.info(f"Upload complete. File URI: {file_url}")

        field_mapping = [
            {
                'Column': [
                    {
                        dict(Number=df.columns.get_loc(col),
                             Field=col)
                    }
                ]
            } if col in system_fields else {
                'Column': [
                    dict(Number=df.columns.get_loc(col),
                         Property=custom_fields[col])
                ]
            } for col in df.columns
        ]

        data = {
            'Source': {
                'Url': self.sftp_host,
                'Username': self.sftp_user,
                'Password': self.sftp_pw
            },
            'Target': {
                'Name': import_name,
                'SubscriberList': list_id
            },
            'ImportSetup': {
                'Mode': import_mode,
                'StartingLine': 1,
                'AllowImportingUnsubscribedEmail': allow_import_unsubscribed,
                'AllowImportingRemovedByUiEmail': allow_import_removed,
                'Mapping': field_mapping
            }
        }

        r_dict = self.client._es_post_request(f'{self.client.api_url}ImportToListTasks', data)
        return r_dict['ApiResponse']['Data']
