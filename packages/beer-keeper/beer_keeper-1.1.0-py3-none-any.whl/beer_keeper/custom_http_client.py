"""Module contains ClientInterface abstract class and RealClient."""
import typing
from abc import ABC
from abc import abstractmethod

import requests


class ClientInterface(ABC):
    """Class has to be extended in order to provide a suitable client for BeerKeeper."""

    @abstractmethod
    def get(self, url, params: typing.Dict = None):
        """
        Abstract Get function. Should return an object which is compatible with requests.models.Response or httpx similar.

        Parameters
        ----------
        url : str
            URL to be accessed by the function.
        params : typing.Dict, optional
            Optional parameters for the get request.
        """
        pass


class RealClient(ClientInterface):
    """Concrete implementation of ClientInterface."""

    def get(self, url, params: typing.Dict = None):
        """Emulates get function from requests lib."""
        return requests.get(url, params=params)
