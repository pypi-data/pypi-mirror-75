# -*- coding: utf-8 -*-

""" Identity class

    Encapsulates the logic to handle JWT tokens
"""

import logging

from jwt.exceptions import InvalidTokenError
import jwt


class Identity:
    """ Holds the identity of the logged user
    """
    def __init__(self, token):
        self._token = token
        try:
            self._decoded = jwt.decode(self._token, verify=False)
        except InvalidTokenError:
            raise ValueError('Invalid JWT token')

    def user_id(self):
        """ Returns the user_id provided by firebase
        """
        return self._decoded.get('user_id')

    def is_system_admin(self):
        """ Returns a boolean identifying the user as a system administrator
        """
        return 'sysadmin' in self._roles()

    def is_admin(self):
        """ Returns a boolean identifying the user 
            as an organization administrator
        """
        return 'admin' in self._roles()

    def is_staff(self):
        """ Returns a boolean identifying the user 
            as a shop staff
        """
        return 'staff' in self._roles()

    def shops(self):
        """ Returns a list of shop_ids that the user has access to
        """
        return self._custom_claims().get('shop', [])

    def organizations(self):
        """ Returns a list of organization_ids that the user has access to
        """
        return self._custom_claims().get('organization', [])

    def data(self):
        """ Return the entire data from the token
        """
        return self._decoded

    def token(self):
        """ Returns the original JWT token
        """
        return self._token

    def _roles(self):
        """ Returns the collection of roles
        """
        if 'claims' not in self._decoded or 'roles' not in self._decoded['claims']:
            logging.error('roles not found')
            return []
        return self._decoded['claims']['roles']

    def _custom_claims(self):
        """ Returns the collection of custom claims
        """
        if 'claims' not in self._decoded or 'claims' not in self._decoded['claims']:
            logging.error('claims not found')
            return {}
        return self._decoded['claims']['claims']
