#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `styler_identity` package."""

from unittest.mock import patch
import pytest


from styler_identity.identity import Identity


class TestIdentity:
    """ Tests 
    """
    def test_invalid_token(self):
        with pytest.raises(ValueError) as expected:
            Identity('invalid token')

        assert str(expected.value) == 'Invalid JWT token'

    def test_valid_token(self, token):
        idem = Identity(token())

        assert isinstance(idem, Identity)

    def test_token(self, token):
        original_token = token()
        idem = Identity(original_token)

        tk = idem.token()

        assert original_token == tk

    def test_user_id(self, token):
        idem = Identity(token({'user_id': '1234'}))

        user_id = idem.user_id()

        assert user_id == '1234'

    def test_is_system_admin(self, token):
        idem = Identity(token({
            'claims': {
                'roles':['sysadmin']
            }
        }))
        idem2 = Identity(token({
            'claims': {
                'roles':['admin']
            }
        }))

        it_should_be = idem.is_system_admin()
        is_should_not_be = idem2.is_system_admin()

        assert it_should_be
        assert not is_should_not_be

    def test_is_admin(self, token):
        idem = Identity(token({
            'claims': {
                'roles':['admin']
            }
        }))
        idem2 = Identity(token({
            'claims': {
                'roles':['staff']
            }
        }))

        it_should_be = idem.is_admin()
        is_should_not_be = idem2.is_admin()

        assert it_should_be
        assert not is_should_not_be

    def test_is_staff(self, token):
        idem = Identity(token({
            'claims': {
                'roles':['staff']
            }
        }))
        idem2 = Identity(token({
            'claims': {
                'roles':['admin']
            }
        }))

        it_should_be = idem.is_staff()
        is_should_not_be = idem2.is_staff()

        assert it_should_be
        assert not is_should_not_be

    @patch('logging.error')
    def test_invalid_roles_sysadmin(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        result = idem.is_system_admin()

        assert not result
        mocked_error.assert_called_once

    @patch('logging.error')
    def test_invalid_roles_admin(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        result = idem.is_admin()

        assert not result
        mocked_error.assert_called_once

    @patch('logging.error')
    def test_invalid_roles_staff(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        result = idem.is_staff()

        assert not result
        mocked_error.assert_called_once

    def test_shops(self, token):
        idem = Identity(token({
            'claims': {
                'claims': {
                    'shop': ['12345', '33442']
                }
            }
        }))

        shops = idem.shops()

        assert shops == ['12345', '33442']

    @patch('logging.error')
    def test_shops_none(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        shops = idem.shops()

        assert shops == []
        mocked_error.assert_called_once

    def test_organizations(self, token):
        idem = Identity(token({
            'claims': {
                'claims': {
                    'organization': ['33333']
                }
            }
        }))

        organizations = idem.organizations()

        assert organizations == ['33333']

    @patch('logging.error')
    def test_organizations_none(self, mocked_error, empty_token):
        idem = Identity(empty_token)

        organizations = idem.organizations()

        assert organizations == []
        mocked_error.assert_called_once

    def test_data(self, token):
        idem = Identity(token())
        expected_keys = {
            'claims',
            'iss',
            'aud',
            'auth_time',
            'user_id',
            'sub',
            'iat',
            'exp',
            'email',
            'email_verified',
            'firebase'
        }

        data = idem.data()

        assert set(data.keys()) == expected_keys
