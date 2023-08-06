"""Contains custom exceptions."""


class BaseException(Exception):
    """Parent exception, inherited by all other custom exceptions."""

    def __init__(self, message: str):
        self.message = message


class BeerNotFoundError(BaseException):
    """Exception raised when the Punk API cannot find a beer with given ID or there is a similar problem."""

    pass


class InvalidQueryParamsError(BaseException):
    """Exception raised when the response object's status code is 400."""

    pass


class InvalidAttemptError(BaseException):
    """Exception raised when trying to make more than 3600 requests per hour to the Punk API."""

    def __init__(self, message="Sorry, you can do 3600 calls/h. Try again later."):
        self.message = message


class InvalidCustomHttpClient(BaseException):
    """Exception raised when trying to give an invalid client to the BeerKeeper class via the http_client attribute."""

    pass
