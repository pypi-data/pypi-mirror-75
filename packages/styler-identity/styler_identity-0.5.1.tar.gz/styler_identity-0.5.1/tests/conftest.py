
import pytest
import jwt


@pytest.fixture
def token():
    def generate(overwrites=None):
        if overwrites is None:
            overwrites = {}
        data = {**{
            'claims': {
                'roles': [],
                'claims': {
                    'shops': [],
                    'organizations': []
                }
            },
            'iss': 'issuer',
            'aud': 'audition',
            'auth_time': 'time',
            'user_id': '1234',
            'sub': 'sub',
            'iat': 1595838390,
            'exp': 1595839390,
            'email': 'email@test.com',
            'email_verified': False,
            'firebase': {
                'identities': {
                    'email': ['email@test.com']
                },
                'sign_in_provider': 'custom'
            }
        }, **overwrites}
        return jwt.encode(data, 'secret-key')
    return generate


@pytest.fixture
def empty_token():
    return jwt.encode({}, 'secret-key')