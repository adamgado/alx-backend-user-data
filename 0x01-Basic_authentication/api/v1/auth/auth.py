#!/usr/bin/env python3
"""template for all authentication system"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded: List[str]) -> bool:
        """return True if the path is not in the list of strings excluded"""
        if path is None:
            return True
        if excluded is None or not excluded:
            return True
        for a in excluded:
            if fnmatch.fnmatch(path, a):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """return the value of the header request Authorization"""
        if request is not None:
            return request.headers.get('Authorization', None)
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get user"""
        return None
