"""Module contains the BeerKeeper class."""
import json
import logging
import typing
from dataclasses import asdict
from typing import Generator
from typing import List

import httpx
import requests
from beer_keeper import custom_exceptions
from beer_keeper.beer import Beer
from beer_keeper.my_http_client import ClientInterface

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
)

logger = logging.getLogger(__name__)


class BeerKeeper:
    """
    Class for main BeerKeeper functionality.

    Returns
    -------
    BeerKeeper object


    Raises
    ------
    custom_exceptions.InvalidAttemptError
    custom_exceptions.InvalidQueryParamsError
    custom_exceptions.BeerNotFoundError
    custom_exceptions.InvalidQueryParamsError

    """

    ENDPOINT = "https://api.punkapi.com/v2/beers"

    def __init__(self, http_client=requests):
        """
        Build object with custom http client.

        Parameters
        ----------
        http_client : [type], optional
            The custom client, by default requests
        """
        if http_client not in [requests, httpx] and not isinstance(
            http_client, ClientInterface
        ):
            raise custom_exceptions.InvalidCustomHttpClient(
                "Trying to give an invalid client to the BeerKeeper."
            )

        self.http_client = http_client
        self.remaining_calls = 3600

    def get_request(self, url, params: typing.Dict = None) -> List[dict]:
        """
        Call instead of requests.get() or httpx.get().

        Parameters
        ----------
        url : string
            The URL of the request
        params : dict, optional
            The parameters of the request, by default None

        Returns
        -------
        list of dicts
            The json of the response in list of dicts form.
        """
        response = self.http_client.get(url, params=params)
        self.check_response(response)

        return response.json()

    def check_response(self, response_obj: object):
        """
        Check if the response's status code is ok and raise an exception accordingly.

        Parameters
        ----------
        response_obj : Response
            Output of the get function (object which is compatible with requests.models.Response or httpx similar).

        Raises
        ------
        custom_exceptions.InvalidAttemptError
        custom_exceptions.InvalidQueryParamsError
        custom_exceptions.BeerNotFoundError
        """
        r_header = response_obj.headers
        r_json = response_obj.json()

        # check attempts
        self.remaining_calls = int(r_header.get("x-ratelimit-remaining"))
        if self.remaining_calls == 0:
            logger.error(
                f"Exception InvalidAttemptError, Remaining attempts: {self.remaining_calls}"
            )
            raise custom_exceptions.InvalidAttemptError()

        # check status code
        status_code = response_obj.status_code
        if status_code == 400:
            error_message = r_json.get("message")
            logger.error(error_message)
            raise custom_exceptions.InvalidQueryParamsError(error_message)
        if status_code == 404:
            error_message = r_json.get("message")
            logger.error(error_message)
            raise custom_exceptions.BeerNotFoundError(error_message)

    def get_beer(self, beer_id: int) -> Beer:
        """
        Make a request and receives beer data for a beer with id beer_id.

        Parameters
        ----------
        beer_id : int
            the ID of a beer from the Punk API

        Returns
        -------
        Beer
            beer.Beer: the Beer object constructed from the data given by the Punk API
        """
        logger.info(f"Getting beer with id: {beer_id}")
        req_url = self.ENDPOINT + "/" + str(beer_id)
        beers = self.get_request(req_url)

        beer_characteristics = beers[0]
        my_beer = Beer(**beer_characteristics)

        return my_beer

    def get_random_beer(self):
        """
        Get a random beer from the Punk API.

        Returns
        -------
        Beer
            A Beer object.
        """
        logger.info("Getting random beer")
        return self.get_beer("random")

    def get_all_beers_from_page(
        self, page_number: int = 1, per_page: int = 25, given_params: typing.Dict = {}
    ) -> list:
        """
        Get beer information from a specified page, the page having a specified size.

        Parameters
        ----------
        page_number : int
            The page number from where to get the information.
        per_page : int, optional
            Specify how many beers are wanted per page. Defaults to 25.
        given_params: typing.Dict
            Extra parameters apart from page and per_page (ex. abv_gt)

        Returns
        -------
        list
            A list of Beer objects constructed from the information given by the Punk API

        Raises
        ------
        custom_exceptions.InvalidQueryParamsError
        """
        logger.info(
            f"Getting all beers from page {page_number}, beers per page: {per_page}, params: {given_params}"
        )

        given_params["page"] = str(page_number)
        given_params["per_page"] = str(per_page)
        beers = self.get_request(self.ENDPOINT, params=given_params)

        beers_on_page = []
        for beer_characteristics in beers:
            a_beer = Beer(**beer_characteristics)
            beers_on_page.append(a_beer)

        return beers_on_page

    def get_all_beers_generator(
        self, given_params: typing.Dict = {}
    ) -> Generator[Beer, None, None]:
        """
        Get a generator containing all the beers from the Punk API, as Beer objects.

        Parameters
        ----------
        given_params: typing.Dict
            Extra parameters apart from page and per_page (ex. abv_gt)

        Yields
        ------
        Generator[Beer, None, None]
            A generator containing Beer objects.
        """
        page_number = 1
        beers_per_page = 80
        while True:
            beers_on_page = self.get_all_beers_from_page(
                page_number, beers_per_page, given_params=given_params
            )
            page_number += 1
            for single_beer in beers_on_page:
                yield single_beer

            if len(beers_on_page) < beers_per_page:
                break

    def get_all_beers(self, given_params: typing.Dict = {}) -> list:
        """
        Get a list containing all the beers from the Punk API, as beer objects.

        Parameters
        ----------
        given_params: typing.Dict
            Extra parameters apart from page and per_page (ex. abv_gt)

        Returns
        -------
        list
            A list containing Beer objects.
        """
        beer_generator = self.get_all_beers_generator(given_params=given_params)
        return [beer for beer in beer_generator]

    def get_beers_by_abv(self, abv_index: float, greater: bool = True) -> list:
        """
        Get a list of beers with alchohol by volume (abv) greater or lower than the abv_index provided.

        Parameters
        ----------
        abv_index : float
            ABV index for comparison.
        greater : bool, optional
            Boolean flag to toggle between greater/lower abv

        Returns
        -------
        list
            A list of Beer objects with the above defined properties
        """
        if greater:
            params = {"abv_gt": str(abv_index)}
        else:
            params = {"abv_lt": str(abv_index)}

        beers = self.get_all_beers(given_params=params)
        return beers

    def get_beers_by_ibu(self, ibu_index: float, greater: bool = True) -> list:
        """
        Get a list of beers with international bittering unit (ibu) greater or lower than the ibu_index provided.

        Parameters
        ----------
        ibu_index : float
            IBU index for comparison.
        greater : bool, optional
            Boolean flag to toggle between greater/lower ibu

        Returns
        -------
        list
            A list of Beer objects with the above defined properties
        """
        if greater:
            params = {"ibu_gt": str(ibu_index)}
        else:
            params = {"ibu_lt": str(ibu_index)}

        beers = self.get_all_beers(given_params=params)
        return beers
