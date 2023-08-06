"""
This is intended to be a server-side client to help with HackRU services that piggyback on lcs login and user data
"""
from typing import Dict, Callable, List

import requests

__version__ = "2.0.0"

LCS_ROOT_URL: str = 'https://api.hackru.org'


def set_root_url(url: str) -> None:
    """Sets root url. defaults to `https://api.hackru.org`"""
    # this is annoying but gets the autogen docs to work
    global LCS_ROOT_URL
    LCS_ROOT_URL = url


TESTING: bool = False


def set_testing(testing: bool) -> None:
    """Whether or not to use test endpoint, defaults to `False`"""
    # this is annoying but gets the autogen docs to work
    global TESTING
    TESTING = testing


class User:
    """
    A user object to easily call other endpoints on behalf of a user
    """

    def __init__(self, email: str = None, password: str = None, token: str = None) -> None:
        """
        Constructor logs the user and gets a handle. Requires you to pass a token OR an email and password
        """
        if not token and not (email and password):
            raise Exception('Must provide either a token, or email and password to login')

        if password:
            self.token = login(email=email, password=password)
            self.email = email

        if token:
            user_profile = validate_token(token=token)
            self.token = token
            self.email = user_profile['email']

    def profile(self) -> Dict:
        """Call lcs to get the user's profile"""
        return get_profile(auth_token=self.token, user_email=self.email)

    def create_dm_link_to(self, other_user_email: str):
        """Get a link to a slack DM between this User and another user identified by `other_user_email`"""
        return create_dm_link_between(token=self.token, other_user_email=other_user_email)


class ResponseError(Exception):
    """Error with an attached HTTP Response"""

    def __init__(self, response: requests.models.Response) -> None:
        self.response = response
        if response.status_code == 200:
            self.status_code = response.json()['statusCode']
        else:
            self.status_code = response.status_code

    def __str__(self) -> str:
        return 'status: %d response: %s' % (self.status_code, self.response.json())


class InternalServerError(ResponseError):
    """An error occurred which prevented LCS from servicing the request"""

    @staticmethod
    def check(response: requests.models.Response) -> None:
        if response.status_code >= 500 or response.json().get('statusCode', 200) >= 500:
            raise InternalServerError(response)


class RequestError(ResponseError):
    """Ideally you shouldn't receive this. There was an issue with the input to the API"""

    @staticmethod
    def check(response: requests.models.Response) -> None:
        if response.status_code == 400 or response.json().get('statusCode', 200) == 400:
            raise RequestError(response)


class CredentialError(RequestError):
    """There was an issue login in with that credential, or a token is invalid"""

    @staticmethod
    def check(response: requests.models.Response) -> None:
        if response.status_code == 403 or response.json().get('statusCode', 200) == 403:
            raise CredentialError(response)


def _check_response(response: requests.models.Response) -> None:
    InternalServerError.check(response)
    RequestError.check(response)
    CredentialError.check(response)


_login_hooks: List[Callable] = []


def on_login(fn: Callable):
    """
    Decorator. Call the decorated function whenever we find a new user
    Use case: get their profile and update local db.
    Function should take in the user object as the first param

    ```python
    @lcs_client.on_login
    def your_func(user_profile):
        # updating the user profile or something
    ```
    """
    global _login_hooks
    _login_hooks.append(fn)
    return fn


def call_login_hooks(user_profile: Dict) -> None:
    for hook in _login_hooks:
        hook(user_profile)


def login(email: str, password: str) -> str:
    """Gets an authentication token by calling the `authorize` LCS endpoint"""
    data = {'email': email, 'password': password}
    response = post(endpoint='/authorize', json=data)

    _check_response(response)
    result = response.json()
    token = result['body']['token']

    call_login_hooks(get_profile(auth_token=token))

    return token


def validate_token(token: str) -> Dict:
    """Validates a lcs token"""
    # else we need to check with lcs and call login hooks
    data = {'token': token}
    response = post(endpoint='/validate', json=data)
    _check_response(response)
    result = response.json()
    user_profile = result['body']
    call_login_hooks(user_profile)
    return user_profile


def get_profile(auth_token: str, user_email: str = None) -> Dict:
    """
    Gets the profile of a user associated with user_email. The permissions associated with the auth_token user are used.
    If no user_email is specified or the user doesn't have enough privilege to view someone else's profile,
    the profile associated with the auth_token is fetched
    """

    data = {'token': auth_token}
    if user_email is not None:
        data['query'] = {'email': user_email}
    response = post(endpoint='/read', json=data)

    _check_response(response)
    return response.json()['body'][0]


def create_dm_link_between(token: str, other_user_email: str) -> str:
    """
    Get a dm link to talk with another user on slack
    """
    data = {'token': token, 'other_email': other_user_email}
    response = post(endpoint='/slack-dm', json=data)
    _check_response(response)
    return response.json()['body']['slack_dm_link']


def get_base_url() -> str:
    """Get the LCS base url"""
    if TESTING:
        return LCS_ROOT_URL + '/dev'
    else:
        return LCS_ROOT_URL + '/prod'


def get(endpoint: str, *args, **kwargs) -> requests.models.Response:
    """Performs a GET request to a LCS endpoint"""
    return requests.get(url=get_base_url() + endpoint, *args, **kwargs)


def post(endpoint: str, *args, **kwargs) -> requests.models.Response:
    """Performs a POST request to a LCS endpoint"""
    return requests.post(url=get_base_url() + endpoint, *args, **kwargs)
