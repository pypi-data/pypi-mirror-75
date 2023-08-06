import requests
from requests import auth

from cloud_control_common.config import api_urls, context_path, api_version, my_user_path


class HttpClient:

    def __init__(self, geo, credentials, org_id=None):
        self._session = requests.Session()
        self._session.auth = auth.HTTPBasicAuth(credentials.get_username(), credentials.get_password())
        self._session.verify = True
        self._session.headers = {'Content-Type': 'application/json'}
        self.host = api_urls.get(geo)
        self.geo = geo
        self.org_id = None
        if org_id is None:
            self.my_user_response = self._validate_credentials_and_get_org_id()
            if self.my_user_response is not None:
                self.org_id = self.my_user_response['organization']['id']
        else:
            self.org_id = org_id

    def get_my_user_response(self):
        return self.my_user_response

    def get_org_id(self):
        return self.org_id

    def post(self, url, credentials):
        pass

    def get(self, path, **kwargs):
        response = self._session.get('{0}{1}'.format(self._get_base_path(), path))
        if response.status_code != 200:
            self._report_error_status(response)
        else:
            return response.json()

    def get_all_available_pages(self, path, query_params=None):
        paginated_response = self._session.request('GET',
                                                   '{0}{1}'.format(self._get_base_path(), path), params=query_params)
        if paginated_response.status_code != 200:
            self._report_error_status(paginated_response)
        else:
            json = paginated_response.json()
            yield json

            json = json or {}

            while json.get('pageCount') >= json.get('pageSize'):
                filters = {'pageNumber': int(json.get('pageNumber')) + 1}
                if query_params:
                    filters.update(query_params)
                paginated_response = self._session.request('GET', '{0}{1}'.format(self._get_base_path(), path),
                                                           params=filters)
                json = paginated_response.json()
                yield json

    def get_with_filters(self, path, query_params):
        response = self._session.request('GET', '{0}{1}'.format(self._get_base_path(), path), params=query_params)
        if response.status_code != 200:
            self._report_error_status(response)
        else:
            return response.json()

    def _validate_credentials_and_get_org_id(self):
        response = self._session.get('{0}/{1}/{2}{3}'
                                     .format(self.host, context_path, api_version, my_user_path))
        if response.status_code != 200:
            return None
        else:
            return response.json()

    def _get_base_path(self):
        return '{0}/{1}/{2}/{3}'.format(self.host, context_path, api_version, self.org_id)

    def _report_error_status(self, response):
        if response.status_code == 401:
            raise Exception(
                'Supplied credentials are incorrect or user is not associated with this geo {0}.'.format
                (self.geo))
        else:
            raise Exception(
                'API call to {0} failed with status code {1}'.format(response.request.url, response.status_code))
