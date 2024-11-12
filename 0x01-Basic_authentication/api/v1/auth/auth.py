#!/usr/bin/env python3
"""template for all authentication system"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return True if the path is not in the list of strings excluded"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        for excluded in excluded_paths:
            if fnmatch.fnmatch(path, excluded):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """return the value of the header request Authorization"""
        if request is not None:
            return request.headers.get('Authorization', None)
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get user from request"""
        return None
