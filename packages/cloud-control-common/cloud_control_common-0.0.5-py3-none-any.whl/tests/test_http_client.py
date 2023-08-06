from unittest.mock import patch, call

import pytest
from requests import Response

from cloud_control_common.credentials import Credentials
from cloud_control_common.http_client import HttpClient


@pytest.fixture()
def event():
    event = {'credentials': {'username': 'myUser', 'password': 'myPassword!', 'api_location': 'africa'}}
    return event


@pytest.fixture
@patch('requests.Session.get')
def http_client(mock_http_get, event, organization_id, request):
    my_user_response = Response()
    my_user_response.status_code = 200
    my_user_response._content = b'{"userName":"roc","organization":{"id": "org_id"}}'
    mock_http_get.return_value = my_user_response

    credentials = Credentials(event)
    http_client = HttpClient('africa', credentials)
    assert http_client.get_my_user_response()['organization']['id'] == 'org_id'

    mock_http_get.assert_called_once_with('https://afapi.opsourcecloud.net/caas/2.13/user/myUser')

    return http_client


@pytest.fixture()
def organization_id():
    return 'org_id'


@patch('requests.Session.get')
def test_get(mock_http_get, http_client):
    response = Response()
    response.status_code = 200
    response._content = b'{"id":"server_id"}'
    mock_http_get.return_value = response
    http_client.get('/server/server')
    mock_http_get.assert_called_once_with('https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server')


@patch('requests.Session.get')
def test_get_401(mock_http_get, http_client):
    response = Response()
    response.status_code = 401
    mock_http_get.return_value = response
    with pytest.raises(Exception):
        http_client.get('/server/server')


@patch('requests.Session.get')
def test_get_500(mock_http_get, http_client):
    response = Response()
    response.status_code = 500
    mock_http_get.return_value = response
    with pytest.raises(Exception):
        http_client.get('/server/server')


@patch('requests.Session.request')
def test_get_all_available_pages(mock_http_request, http_client):
    first_page = Response()
    first_page.status_code = 200
    first_page._content = b'{"server":[{"id":"server_id1"}],"pageNumber": 1, "pageCount": 1,  "totalCount": 2, ' \
                          b'"pageSize": 1}'

    second_page = Response()
    second_page.status_code = 200
    second_page._content = b'{"server":[{"id":"server_id2"}],"pageNumber": 2, "pageCount": 1,  "totalCount": 2, ' \
                           b'"pageSize": 1}'
    mock_http_request.side_effect = [first_page, second_page]
    pages = http_client.get_all_available_pages('/server/server')
    next(pages)
    next(pages)

    calls = [call('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server', params=None),
             call('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server', params={'pageNumber': 2})]

    mock_http_request.assert_has_calls(calls)


@patch('requests.Session.request')
def test_get_all_available_pages_only_1_page(mock_http_request, http_client):
    first_page = Response()
    first_page.status_code = 200
    first_page._content = b'{"server":[{"id":"server_id1"}],"pageNumber": 1, "pageCount": 1,  "totalCount": 1, ' \
                          b'"pageSize": 1}'

    mock_http_request.return_value = first_page
    pages = http_client.get_all_available_pages('/server/server')
    next(pages)
    mock_http_request.assert_called_once_with('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server',
                                              params=None)


@patch('requests.Session.request')
def test_get_all_available_pages_401(mock_http_request, http_client):
    response = Response()
    response.status_code = 401
    mock_http_request.return_value = response

    with pytest.raises(Exception):
        next(http_client.get_all_available_pages('/server/server'))

    mock_http_request.assert_called_once_with('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server',
                                              params=None)


@patch('requests.Session.get')
def test_validate_credentials_and_get_org_id(mock_http_get, http_client):
    response = Response()
    response.status_code = 200
    response._content = b'{"userName":"roc","organization":{"id": "response_org_id"}}'
    mock_http_get.return_value = response
    http_client._validate_credentials_and_get_org_id()
    mock_http_get.assert_called_once_with('https://afapi.opsourcecloud.net/caas/2.13/user/myUser')


@patch('requests.Session.get')
def test_validate_credentials_and_get_org_id_invalid(mock_http_get, event):
    my_user_response = Response()
    my_user_response.status_code = 400
    mock_http_get.return_value = my_user_response

    credentials = Credentials(event)
    client = HttpClient('specified_geo', credentials)
    assert client.get_my_user_response() is None
    assert client._validate_credentials_and_get_org_id() is None


@patch('requests.Session.request')
def test_get_with_filters(mock_http_request, http_client):
    page = Response()
    page.status_code = 200
    page._content = b'{"server":[{"id":"server_id1"}],"pageNumber": 1, "pageCount": 1,  "totalCount": 1, ' \
                    b'"pageSize": 1}'

    mock_http_request.return_value = page
    pages = http_client.get_with_filters('/server/server', {'id': ['uuid']})
    mock_http_request.assert_called_once_with('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server',
                                              params={'id': ['uuid']})


@patch('requests.Session.request')
def test_get_with_filters_401(mock_http_request, http_client):
    response = Response()
    response.status_code = 401
    mock_http_request.return_value = response

    with pytest.raises(Exception):
        http_client.get_with_filters('/server/server', {'id': ['uuid']})

    mock_http_request.assert_called_once_with('GET', 'https://afapi.opsourcecloud.net/caas/2.13/org_id/server/server',
                                              params={'id': ['uuid']})
