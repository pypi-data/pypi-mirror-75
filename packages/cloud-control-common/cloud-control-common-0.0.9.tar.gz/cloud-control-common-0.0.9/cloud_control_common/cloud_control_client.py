from cloud_control_common.config import list_servers, list_network_domains, list_tags, list_datacenters, list_os_image, \
    list_customer_image, list_geos
from cloud_control_common.http_client import HttpClient


class CloudControlClient:

    def __init__(self, credentials, geo, org_id=None):
        self.credentials = credentials
        self.geo = geo
        self.http_client = HttpClient(geo, self.credentials, org_id=org_id)
        self.home_geo = None

    def validate_credentials(self):
        my_user = self.http_client.get_my_user_response()
        if not my_user:
            return None
        self.home_geo = my_user['organization']['homeGeoId']
        return my_user

    def get_home_geo(self):
        return self.home_geo

    def get_all_servers(self):
        return self.__get_all_available_of_type(list_servers, 'server')

    def get_servers(self, event):
        return self.http_client.get_with_filters(list_servers, event)

    def get_all_tags(self, filters=None):
        return self.__get_all_available_of_type(list_tags, 'tag', filters)

    def get_tags(self, event):
        return self.http_client.get_with_filters(list_tags, event)

    def get_all_network_domains(self):
        return self.__get_all_available_of_type(list_network_domains, 'networkDomain')

    def get_datacenters(self, event):
        return self.http_client.get_with_filters(list_datacenters, event)

    def get_all_datacenters(self):
        return self.__get_all_available_of_type(list_datacenters, 'datacenter')

    def get_all_os_images(self):
        os_images = self.__get_all_available_of_type(list_os_image, 'osImage')
        return os_images

    def get_all_customer_images(self):
        customer_images = self.__get_all_available_of_type(list_customer_image, 'customerImage')
        return customer_images

    def get_all_geos(self):
        geos = self.__get_all_available_of_type(list_geos, 'geographicRegion')
        return geos

    def get_org_id(self):
        return self.http_client.get_org_id()

    def __get_all_available_of_type(self, path, response_type, query_params=None):
        paginated = self.http_client.get_all_available_pages(path, query_params)
        return self.__convert_to_response_types(paginated, response_type)

    @staticmethod
    def __convert_to_response_types(paginated, response_type):
        response_types = []
        for result in paginated:
            for element in result[response_type]:
                response_types.append(element)
        return response_types

    @staticmethod
    def get_api_location(event):
        return event.get('credentials').get('api_location')
