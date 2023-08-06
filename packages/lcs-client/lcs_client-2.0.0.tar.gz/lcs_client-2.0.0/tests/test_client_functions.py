import pytest

import lcs_client
from tests.testing_utils import *


def test_set_testing():
    curr_val = lcs_client.TESTING
    lcs_client.set_testing(testing=not curr_val)
    assert lcs_client.TESTING == (not curr_val)
    lcs_client.set_testing(testing=curr_val)


def test_set_root_url():
    curr_url = lcs_client.LCS_ROOT_URL
    lcs_client.set_root_url(url=TEST_URL)
    assert lcs_client.LCS_ROOT_URL == TEST_URL
    lcs_client.set_root_url(url=curr_url)


def test_get_base_url():
    curr_testing_val = lcs_client.TESTING
    curr_base_url = lcs_client.get_base_url()
    lcs_client.set_testing(testing=not curr_testing_val)
    new_base_url = lcs_client.get_base_url()
    lcs_client.set_testing(testing=curr_testing_val)
    assert curr_base_url != new_base_url


def test_get(mocker):
    mocker.patch('requests.get', lambda url, *args, **kwargs: MockResponse.OK)
    resp = lcs_client.get(endpoint='')
    assert resp.status_code == 200
    assert resp.json()['statusCode'] == 200


def test_post(mocker):
    mocker.patch('requests.post', lambda url, *args, **kwargs: MockResponse.OK)
    resp = lcs_client.post('')
    assert resp.status_code == 200
    assert resp.json()['statusCode'] == 200


def test_check_response():
    lcs_client._check_response(response=MockResponse.OK)


def test_internal_server_error():
    error_response = MockResponse(200, {'statusCode': 500})
    with pytest.raises(lcs_client.InternalServerError):
        lcs_client._check_response(response=error_response)
    error_response = MockResponse(500, {})
    with pytest.raises(lcs_client.InternalServerError):
        lcs_client._check_response(response=error_response)


def test_request_error():
    error_response = MockResponse(200, {'statusCode': 400})
    with pytest.raises(lcs_client.RequestError):
        lcs_client._check_response(response=error_response)
    error_response = MockResponse(400, {})
    with pytest.raises(lcs_client.RequestError):
        lcs_client._check_response(response=error_response)


def test_credential_error():
    error_response = MockResponse(200, {'statusCode': 403})
    with pytest.raises(lcs_client.CredentialError):
        lcs_client._check_response(response=error_response)
    error_response = MockResponse(403, {})
    with pytest.raises(lcs_client.CredentialError):
        lcs_client._check_response(response=error_response)


def test_add_login_hook():
    @lcs_client.on_login
    def call():
        return True

    assert lcs_client._login_hooks[-1] == call
    lcs_client._login_hooks.remove(call)


def test_call_login_hooks():
    test_profile = {
        'num': 10
    }

    def modify_profile(profile):
        profile['major'] = 'undecided'
        profile['new_num'] = profile['num'] + 50

    lcs_client._login_hooks.append(modify_profile)
    lcs_client.call_login_hooks(user_profile=test_profile)
    assert test_profile['major']
    assert test_profile['new_num'] == 60
    lcs_client._login_hooks.remove(modify_profile)


def test_login(mocker):
    login_mock_response = MockResponse(200, {'statusCode': 200, 'body': {'token': TEST_TOKEN}})
    mocker.patch('lcs_client.post', lambda endpoint, json: login_mock_response)
    mocker.patch('lcs_client.call_login_hooks', lambda _: None)
    mocker.patch('lcs_client.get_profile', lambda auth_token: None)
    token = lcs_client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
    assert token == TEST_TOKEN


def test_validate_token(mocker):
    validate_mock_response = MockResponse(200, {'statusCode': 200, 'body': TEST_PROFILE})
    mocker.patch('lcs_client.post', lambda endpoint, json: validate_mock_response)
    mocker.patch('lcs_client.call_login_hooks', lambda _: None)
    usr_profile = lcs_client.validate_token(token=TEST_TOKEN)
    assert usr_profile == TEST_PROFILE
    assert usr_profile['email'] == TEST_EMAIL
    assert usr_profile['token'][0] == TEST_TOKEN


def test_get_profile(mocker):
    get_profile_mock_response = MockResponse(200, {'statusCode': 200, 'body': [TEST_PROFILE]})
    mocker.patch('lcs_client.post', lambda endpoint, json: get_profile_mock_response)
    usr_profile = lcs_client.get_profile(auth_token=TEST_TOKEN)
    assert usr_profile == TEST_PROFILE
    assert usr_profile['email'] == TEST_EMAIL
    assert usr_profile['token'][0] == TEST_TOKEN
    usr_profile = lcs_client.get_profile(auth_token=TEST_TOKEN, user_email=TEST_EMAIL)
    assert usr_profile == TEST_PROFILE
    assert usr_profile['email'] == TEST_EMAIL
    assert usr_profile['token'][0] == TEST_TOKEN


def test_create_dm_link_between(mocker):
    dm_link_mock_response = MockResponse(200, {'statusCode': 200, 'body': {'slack_dm_link': TEST_URL}})
    mocker.patch('lcs_client.post', lambda endpoint, json: dm_link_mock_response)
    dm_link = lcs_client.create_dm_link_between(token=TEST_TOKEN, other_user_email=TEST_EMAIL)
    assert dm_link == TEST_URL
