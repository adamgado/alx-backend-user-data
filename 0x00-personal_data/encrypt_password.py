#!/usr/bin/env python3
"""returns a salted, hashed password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches"""
    return bcrypt.checkpw(password.encode(), hashed_password)
