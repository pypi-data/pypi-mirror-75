"""Module contains CLI functions."""
import argparse
import pprint
from dataclasses import asdict

import httpx
from beer_keeper.client import BeerKeeper
from beer_keeper.custom_http_client import RealClient
from beer_keeper.params import after
from beer_keeper.params import before
from beer_keeper.params import equals
from beer_keeper.params import greater_than
from beer_keeper.params import inside
from beer_keeper.params import less_than
from beer_keeper.params import P
from beer_keeper.params import Param as param


def build_argument_parser():
    """
    Build the argument parser and set the options.

    Returns
    -------
    ArgumentParser object
    """
    argument_parser = argparse.ArgumentParser(
        description="BeerKeeper CLI tool", epilog="Thanks for using our plugin"
    )

    argument_parser.add_argument(
        "--per-page",
        type=int,
        default=25,
        action="store",
        help="Set number of beers to be returned per page. Default per_page=25",
    )

    # group = argument_parser.add_mutually_exclusive_group()

    argument_parser.add_argument(
        "-b",
        "--beer",
        type=int,
        action="store",
        help="Return a single beer by ID. Default beer=1.",
    )

    argument_parser.add_argument(
        "-ag",
        "--abv-gt",
        type=float,
        action="store",
        help="Return all beers with ABV greater than a given value.",
    )

    argument_parser.add_argument(
        "-al",
        "--abv-lt",
        type=float,
        action="store",
        help="Return all beers with ABV lower than a given value.",
    )

    argument_parser.add_argument(
        "-ig",
        "--ibu-gt",
        type=float,
        action="store",
        help="Return all beers with IBU greater than a given value.",
    )

    argument_parser.add_argument(
        "-il",
        "--ibu-lt",
        type=float,
        action="store",
        help="Return all beers with IBU lower than a given value.",
    )

    argument_parser.add_argument(
        "-p",
        "--page",
        type=int,
        action="store",
        help="Return all beers from page. Default page=1",
    )

    argument_parser.add_argument(
        "-r", "--random", action="store_true", help="Return a random beer",
    )

    argument_parser.add_argument(
        "-eg",
        "--ebc-gt",
        type=float,
        action="store",
        help="Return all beers with EBC greater than a given value.",
    )

    argument_parser.add_argument(
        "-el",
        "--ebc-lt",
        type=float,
        action="store",
        help="Return all beers with EBC lower than a given value.",
    )

    argument_parser.add_argument(
        "-bn",
        "--beer-name",
        type=str,
        action="store",
        help="Return all beers matching the supplied name.",
    )

    argument_parser.add_argument(
        "-ye",
        "--yeast",
        type=str,
        action="store",
        help="Return all beers matching the supplied yeast name.",
    )

    argument_parser.add_argument(
        "-bb",
        "--brewed-before",
        type=str,
        action="store",
        help="Return all beers brewed before the given date. Format: MM-YYYY",
    )

    argument_parser.add_argument(
        "-ba",
        "--brewed-after",
        type=str,
        action="store",
        help="Return all beers brewed after the given date. Format: MM-YYYY",
    )

    argument_parser.add_argument(
        "-ho",
        "--hops",
        type=str,
        action="store",
        help="Return all beers matching the supplied hops name.",
    )

    argument_parser.add_argument(
        "-ma",
        "--malt",
        type=str,
        action="store",
        help="Return all beers matching the supplied malt name.",
    )

    argument_parser.add_argument(
        "-fo",
        "--food",
        type=str,
        action="store",
        help="Return all beers matching the supplied food name.",
    )

    return argument_parser


def get_functionality(arguments, a_keeper):
    """
    Extract the right answer using fields.

    Parameters
    ----------
    arguments : namedtuple
        Contains argument options
    a_keeper : BeerKeeper object
        The object with which the functions are called

    Returns
    -------
    Result of the query.
    """
    params = vars(arguments)
    if arguments.random:
        return a_keeper.get_random_beer()
    elif arguments.page is not None:
        return a_keeper.get_all_beers_from_page(
            params=[
                P("page", condition=equals(arguments.page)),
                P("per_page", condition=equals(arguments.per_page)),
            ]
        )
    elif arguments.beer is not None:
        return a_keeper.get_beer(arguments.beer)
    else:
        # clean params
        cleaned_params = {}
        for key, value in params.items():
            if value is not None and key not in ["random", "beer"]:
                cleaned_params[key] = value
        print(cleaned_params)
        return a_keeper.get_all_beers(params=cleaned_params)
    # elif arguments.abv_greater is not None:
    #     return a_keeper.get_all_beers(
    #         params=[P("abv", condition=greater_than(arguments.abv_greater))]
    #     )
    # elif arguments.abv_lower is not None:
    #     return a_keeper.get_all_beers(
    #         params=[P("abv", condition=less_than(arguments.abv_lower))]
    #     )
    # elif arguments.ibu_greater is not None:
    #     return a_keeper.get_all_beers(
    #         params=[P("ibu", condition=greater_than(arguments.ibu_greater))]
    #     )
    # elif arguments.ibu_lower is not None:
    #     return a_keeper.get_all_beers(
    #         params=[P("ibu", condition=less_than(arguments.ibu_lower))]
    #     )
    # else:
    #     return a_keeper.get_all_beers(params={})


def display_pretty(result):
    """
    Print in a pretty way the result.

    Parameters
    ----------
    result  : Beer of list of Beer
        Answer of the solve_functionality() function

    Returns
    -------
    Nothing
    """
    if isinstance(result, list):
        for a_beer in result:
            pprint.pprint(asdict(a_beer))
    else:
        pprint.pprint(asdict(result))


def app():
    """
    Call to exhibit the behaviour of the CLI.

    Returns
    -------
    Nothing
    """
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    a_keeper = BeerKeeper(http_client=RealClient())
    result = get_functionality(arguments, a_keeper)
    display_pretty(result)


if __name__ == "__main__":
    app()
