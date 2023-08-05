import json
import os
from unittest.mock import patch

import pytest

from cloud_control_common.cloud_control_client import CloudControlClient
from cloud_control_common.credentials import Credentials

module_dir = os.path.dirname(__file__)


@pytest.fixture()
def event():
    event = {'credentials': {'username': 'myUser', 'password': 'myPassword!', 'api_location': 'northamerica'}}
    return event


@pytest.fixture()
@patch('cloud_control_common.http_client.HttpClient._validate_credentials_and_get_org_id')
def cloud_control_client(mock_http_client_function, event):
    json_file = open(os.path.join(module_dir, 'json/my_user.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)
    return CloudControlClient(Credentials(event), 'northamerica')


@patch('cloud_control_common.http_client.HttpClient.get_my_user_response')
def test_validate_credentials(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/my_user.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)
    my_user = cloud_control_client.validate_credentials()
    assert my_user is not None
    assert cloud_control_client.home_geo == 'dev_geo1'


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_servers(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/servers_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_servers()
    mock_http_client_function.assert_called_once_with("/server/server", None)
    assert len(of_type) == 2


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_servers_empty(mock_http_client_function, cloud_control_client):
    mock_http_client_function.return_value = [
        {
            "server": [],
            "pageNumber": 1,
            "pageCount": 0,
            "totalCount": 0,
            "pageSize": 0
        }
    ]

    of_type = cloud_control_client.get_all_servers()
    mock_http_client_function.assert_called_once_with("/server/server", None)
    assert len(of_type) == 0


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_tags(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/tags_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_tags()
    mock_http_client_function.assert_called_once_with("/tag/tag", None)
    assert len(of_type) == 6


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_network_domains(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/network_domains_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_network_domains()
    mock_http_client_function.assert_called_once_with("/network/networkDomain", None)
    assert len(of_type) == 11


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_datacenters(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/datacenters_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_datacenters()
    mock_http_client_function.assert_called_once_with("/infrastructure/datacenter", None)
    assert len(of_type) == 4


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_os_images(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/os_images_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_os_images()
    mock_http_client_function.assert_called_once_with("/image/osImage/", None)
    assert len(of_type) == 4


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_customer_images(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/customer_images_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_customer_images()
    mock_http_client_function.assert_called_once_with("/image/customerImage/", None)
    assert len(of_type) == 2


@patch('cloud_control_common.http_client.HttpClient.get_all_available_pages')
def test_get_all_geos(mock_http_client_function, cloud_control_client):
    json_file = open(os.path.join(module_dir, 'json/geo_all_pages.json'), 'r')
    mock_http_client_function.return_value = json.load(json_file)

    of_type = cloud_control_client.get_all_geos()
    mock_http_client_function.assert_called_once_with("/infrastructure/geographicRegion", None)
    assert len(of_type) == 3


def test_get_api_location(event):
    api_location = CloudControlClient.get_api_location(event)
    assert 'northamerica' == api_location
