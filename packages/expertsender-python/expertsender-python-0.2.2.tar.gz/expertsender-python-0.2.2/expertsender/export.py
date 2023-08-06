from abc import ABC
import io
import zipfile

import requests
try:
    import pandas as pd
except ImportError:
    pd = None

from .errors import ExpertsenderExportError


class ExportMixin(ABC):
    """
    Implements all functions regarding the export of subscribers.
    """
    def start_export(self, e_type: str = 'list', list_id: str = '',  segment_id: str = '', fields: list = 'all',
                     properties: list = 'all') -> int:
        """
        Start the export of a list or a segment from Expertsender.
        API doc: https://sites.google.com/site/expertsenderapiv2/methods/start-a-new-export
        :param e_type: Export type. Can either be 'list' or 'segment'
        :param list_id: Only required if export type is 'list'
        :param segment_id: Only required if export type is 'segment'
        :param fields: Either 'all' or a list of Expertsender fields (e.g. Email, Firstname, Vendor etc) to be exported.
        :param properties: Collection of Property elements. List of custom subscriber properties to be exported.
            Properties are identified by ID.
        :return: ID of scheduled export.
        """
        assert e_type in ['list', 'segment'], "The export type has to be either 'list' or 'segment' "
        assert type(fields) == list or fields == 'all'
        assert type(properties) == list or properties == 'all'

        system_fields = [
            'Id', 'FirstName', 'LastName', 'Email', 'EmailMd5', 'EmailSha256',
            'CustomSubscriberId', 'IP', 'Vendor', 'TrackingCode', 'GeoCountry',
            'GeoState', 'GeoCity', 'GeoZipCode', 'LastActivity', 'LastMessage',
            'LastEmail', 'LastOpenEmail', 'LastClickEmail', 'SubscriptionDate'
        ]
        fields = [
            {'Field': f} for f in fields or {}
        ] if type(fields) == list else [
            {'Field': f} for f in system_fields
        ]

        properties = [
            {'Property': f} for f in fields or {}
        ] if type(properties) == list else [
            {'Property': p_id} for p_name, p_id in self.custom_fields().items()
        ]

        data = {
            'Type': e_type.capitalize(),
            'Fields': fields,
            'Properties': properties
        }
        if e_type == 'list':
            data.update({'ListId': str(list_id)})
        else:
            data.update({'SegmentId': str(segment_id)})

        r_dict = self._es_post_request(f'{self.api_url}Exports', data)
        return r_dict['ApiResponse']['Data']

    def get_export_progress(self, process_id) -> dict:
        """
        Method returns an object describing the scheduled export status. If export has completed, URL with file
        to download is also returned.
        :param process_id: Id of the process
        :return: A dict containing key 'Status' with the possible values 'Queued', 'InProgress', 'Completed', 'Error'/
            If status is complete, also has key 'DownloadUrl'
        """
        url = f'{self.api_url}Exports/{process_id}?apiKey={self.api_key}'

        r_dict = self._es_get_request(url)
        return r_dict['ApiResponse']['Data']

    def export_done(self, process_id):
        export = self.get_export_progress(process_id)
        if export['Status'] in {'Queued', 'InProgress'}:
            return False
        elif export['Status'] == 'Completed':
            return True
        elif export['Status'] == 'Error':
            raise ExpertsenderExportError('Export has failed.')
        else:
            # Should never happen
            raise ValueError('Export status return does not follow the required format.')

    def download_export(self, process_id):
        """
        Requires Pandas installed (optional dependency)
        :param process_id: Id of the export process
        :return: Pandas DataFrame containing the requested data
        """
        if not pd:
            raise ImportError('This function requires the Pandas package.')

        export = self.get_export_progress(process_id)
        if export['Status'] in {'Queued', 'InProgress'}:
            raise ExpertsenderExportError('Export still in Progress.')
        elif export['Status'] == 'Error':
            raise ExpertsenderExportError('Export has failed.')
        elif export['Status'] == 'Completed':
            url = export['DownloadUrl']
        else:
            # Should never happen
            raise ValueError('Export status return does not follow the required format.')

        # Expertsender returns the data as a ZIP containing a single file
        res = requests.get(url, stream=True)
        zip_file_object = zipfile.ZipFile(io.BytesIO(res.content))
        first_file = zip_file_object.namelist()[0]
        file = zip_file_object.open(first_file)
        content = file.read()

        # Return data as a pandas DataFrame
        return pd.read_csv(io.BytesIO(content))
