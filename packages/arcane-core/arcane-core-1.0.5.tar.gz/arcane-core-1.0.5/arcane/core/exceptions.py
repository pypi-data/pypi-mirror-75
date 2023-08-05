from google.cloud import exceptions as _exceptions
import requests  # Include in google-cloud-core


GOOGLE_EXCEPTIONS_TO_RETRY = (
    _exceptions.InternalServerError,
    _exceptions.ServerError,
    _exceptions.ServiceUnavailable,
    _exceptions.GatewayTimeout,
    requests.exceptions.ConnectionError,  # Use to make http call in google's client
    ConnectionResetError  # not a Google exception but can happen
)


class Error(Exception):
    """Base class for other exceptions"""
    pass


class IssueSpreadsheetDatabase(Error):
    """Raised when there is an error with the spreadsheets database"""
    def __init__(self, reason: str, message: str, *args):
        self.reason = reason
        self.message = message
        super().__init__(message, reason, *args)


class GCPBucketNotFound(Exception):
    def __init__(self, bucket_name: str, project: str = ""):
        print(f"Bucket {bucket_name} don't exist in project {project} ")


class BadRequestError(Error):
    def __init__(self, message):
        super().__init__(message)


class NotFoundError(Error):
    def __init__(self, message):
        super().__init__(message)
