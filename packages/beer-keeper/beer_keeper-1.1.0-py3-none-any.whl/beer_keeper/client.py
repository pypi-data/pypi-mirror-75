"""Module contains the BeerKeeper class."""
import datetime
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
from beer_keeper.custom_http_client import ClientInterface
from beer_keeper.params import after
from beer_keeper.params import before
from beer_keeper.params import equals
from beer_keeper.params import greater_than
from beer_keeper.params import inside
from beer_keeper.params import less_than
from beer_keeper.params import P
from beer_keeper.params import Param as param


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

    def check_and_refine(self, params):
        """
        Refine params based on its type.

        Parameters
        ----------
        params
            Parameters of a request, can be list[P] or dict

        Returns
        -------
        dict
            The refined params.
        """
        if isinstance(params, list) and all([isinstance(par, P) for par in params]):
            # params is a list made out of P objects
            refined_params = self.refine_params(params)
        elif isinstance(params, dict) and all(
            # params is a dict that is already refined
            [isinstance(key, str) for key in params.keys()]
        ):
            refined_params = params

        return refined_params

    def get_all_beers_from_page(self, params) -> List[Beer]:
        """
        Get beer information from a specified page, the page having a specified size.

        Parameters
        ----------
        page_number : int
            The page number from where to get the information.
        per_page : int, optional
            Specify how many beers are wanted per page. Defaults to 25.
        params: typing.Dict
            Extra parameters apart from page and per_page (ex. abv_gt)

        Returns
        -------
        List[Beer]
            A list of Beer objects constructed from the information given by the Punk API

        Raises
        ------
        custom_exceptions.InvalidQueryParamsError
        """
        refined_params = self.check_and_refine(params)

        page = refined_params["page"]
        per_page = refined_params["per_page"]
        logger.info(
            f"Getting all beers from page {page}, beers per page: {per_page}, params: {params}"
        )

        beers = self.get_request(self.ENDPOINT, params=refined_params)

        beers_on_page = []
        for beer_characteristics in beers:
            a_beer = Beer(**beer_characteristics)
            beers_on_page.append(a_beer)

        return beers_on_page

    def get_all_beers_generator(
        self, params: typing.Dict = {}
    ) -> Generator[Beer, None, None]:
        """
        Get a generator containing all the beers from the Punk API, as Beer objects.

        Parameters
        ----------
        params: typing.Dict
            Extra parameters apart from page and per_page (ex. abv_gt)

        Yields
        ------
        Generator[Beer, None, None]
            A generator containing Beer objects.
        """
        params["page"] = 1
        params["per_page"] = 80
        while True:
            beers_on_page = self.get_all_beers_from_page(params=params)
            params["page"] += 1
            for single_beer in beers_on_page:
                yield single_beer

            if len(beers_on_page) < params["per_page"]:
                break

    def refine_params(self, params: List[P]) -> typing.Dict:
        """
        Refine the parameters by mapping the list of P objects into a dictionary.

        Parameters
        ----------
        params : List[P]
            A list of P objects.

        Returns
        -------
        typing.Dict
            The actual dictionary that can be passed as a parameter to the request.
        """
        refined_params = {}
        for p in params:
            for single_condition in p.get_all_conditions():
                dict_key = str(p.keyword_param) + single_condition[0]
                dict_val = single_condition[1]

                if dict_key in refined_params:  # don't overwrite the value, append it
                    if isinstance(refined_params[dict_key], str):
                        # this is the case where we have ex. params=[P("ids", conditions=[inside([1, 2]), equals(3)])].
                        # Here, inside([1,2]) returns ("", "(|1|2|)") and equals(3) returns ("", 3) => we need "(|1|2|3|)"
                        current_val = refined_params[dict_key]
                        current_val = current_val[:-1]

                        if str(dict_val).startswith("("):
                            # this is the case where we have for ex. params=[P("ids", conditions=[inside([1, 2]), inside([3,4])])].
                            dict_val = dict_val[2:]
                            current_val += dict_val
                        else:
                            current_val += str(dict_val)
                            # this is the case where we have for ex. params=[P("ids", conditions=[inside([1, 2]), equals(3)])].
                            current_val += "|)"
                        refined_params[dict_key] = current_val

                    if isinstance(refined_params[dict_key], int):
                        # this is the case where we have for ex. params=[P("ids", conditions=[equals(1), equals(2)])].
                        current_val = [refined_params[dict_key]]
                        current_val.append(dict_val)
                        refined_params[dict_key] = inside(current_val)[1]

                else:
                    refined_params[dict_key] = dict_val

        return refined_params

    def get_all_beers(self, params={}) -> list:
        """
        Get a list containing all the beers from the Punk API, as beer objects.

        Parameters
        ----------
        params
            Extra parameters apart from page and per_page (ex. abv_gt)

        Returns
        -------
        list
            A list containing Beer objects.
        """
        refined_params = self.check_and_refine(params)

        beer_generator = self.get_all_beers_generator(params=refined_params)
        return [beer for beer in beer_generator]
