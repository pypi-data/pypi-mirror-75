import pytest

import lcs_client
from tests.testing_utils import *


def test_bad_user_no_credentials():
    with pytest.raises(Exception):
        lcs_client.User()


def test_bad_user_missing_email():
    with pytest.raises(Exception):
        lcs_client.User(password=TEST_PASSWORD)


def test_bad_user_missing_password():
    with pytest.raises(Exception):
        lcs_client.User(email=TEST_EMAIL)


def test_successful_user_creation_using_email_password(mocker):
    mocker.patch('lcs_client.login', return_value=TEST_TOKEN)
    usr = lcs_client.User(email=TEST_EMAIL, password=TEST_PASSWORD)
    assert usr.token == TEST_TOKEN
    assert usr.email == 'rnd@hackru.org'


@patch_validate_token
def test_successful_user_creation_using_token(mocker):
    usr = lcs_client.User(token=TEST_TOKEN)
    assert usr.email == TEST_EMAIL
    assert usr.token == TEST_TOKEN


@patch_validate_token
def test_user_get_profile(mocker):
    mocker.patch('lcs_client.get_profile', return_value=TEST_PROFILE)
    usr = lcs_client.User(token=TEST_TOKEN)
    usr_profile = usr.profile()
    assert usr_profile == TEST_PROFILE


@patch_validate_token
def test_user_get_dm_link_for(mocker):
    mocker.patch('lcs_client.create_dm_link_between', return_value=TEST_URL)
    usr = lcs_client.User(token=TEST_TOKEN)
    dm_link = usr.create_dm_link_to(other_user_email='notrnd@hackru.org')
    assert dm_link == TEST_URL
