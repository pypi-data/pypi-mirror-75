TEST_URL = 'https://hackru.org'
TEST_EMAIL = 'rnd@hackru.org'
TEST_PASSWORD = 'letmein'
TEST_TOKEN = 'complexandsecuretoken'
TEST_PROFILE = {
    'email': TEST_EMAIL,
    'token': [
        TEST_TOKEN
    ],
    'major': '',
    'github': '',
    'school': ''
}
TEST_USER = None


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


MockResponse.OK = MockResponse(200, {'statusCode': 200})


def patch_validate_token(fn):
    def wrap(mocker):
        mocker.patch('lcs_client.validate_token', return_value={'email': TEST_EMAIL, 'token': TEST_TOKEN})
        fn(mocker)

    return wrap
