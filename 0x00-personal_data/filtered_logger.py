#!/usr/bin/env python3
"""
Logging module for filtering PII data.
"""

import logging
import re
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates PII fields in a log message.
    """
    for field in fields:
        message = re.sub(
            rf"{field}=.*?{separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


def get_db() -> MySQLConnection:
    """
    Connects to a secure Holberton MySQL database using credentials from
    environment variables and returns a MySQLConnection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that filters sensitive information.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record and redact PII fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Returns a logger named 'user_data' with a custom redacting formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def main() -> None:
    """Main function that fetches and logs user data from the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    # Column names in the table (same order as the SELECT *)
    columns = [desc[0] for desc in cursor.description]

    logger = get_logger()

    for row in cursor:
        # Map column names to values
        # build a log line like key=value; key=value; ...
        row_dict = dict(zip(columns, row))
        log_message = "; ".join(f"{k}={v}" for k, v in row_dict.items()) + ";"
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
