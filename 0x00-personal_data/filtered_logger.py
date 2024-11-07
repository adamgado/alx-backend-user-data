#!/usr/bin/env python3
"""display each row under a filtered format"""
import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for a in fields:
        message = re.sub(a + "=.*?" + separator,
                         a + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    log_obj = logging.getLogger('user_data')
    log_obj.setLevel(logging.INFO)
    log_obj.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    log_obj.addHandler(handler)
    return log_obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    user = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    pas = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    name = environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connection.MySQLConnection(user=user,
                                                     password=pas,
                                                     host=host,
                                                     database=name)
    return db



def main():
    """display each row under a filtered format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [a[0] for a in cursor.description]
    log_obj = get_logger()
    for row in cursor:
        str_row = ''.join(b'{b}={str(a)}; ' for a, b in zip(row, fields))
        log_obj.info(str_row.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
