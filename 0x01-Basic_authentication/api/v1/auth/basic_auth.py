#!/usr/bin/env python3
"""BasicAuth that inherits from Auth"""
import re
import base64
import binascii
from typing import Tuple, TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class"""
    def extract_base64_authorization_header(self,
            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field = re.fullmatch(pattern, authorization_header.strip())
            if field is not None:
                return field.group('token')
        return None

    def decode_base64_authorization_header(self,
            base64_authorization_header: str,
            ) -> str:
        """returns the decoded value of a Base64 string"""
        if type(base64_authorization_header) == str:
            try:
                result = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return result.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """return user email, password from Base64 decoded value"""
        if type(decoded_base64_authorization_header) == str:
            order = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                order,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(self, user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        header = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(header)
        token = self.decode_base64_authorization_header(b64_token)
        email, password = self.extract_user_credentials(token)
        return self.user_object_from_credentials(email, password)
