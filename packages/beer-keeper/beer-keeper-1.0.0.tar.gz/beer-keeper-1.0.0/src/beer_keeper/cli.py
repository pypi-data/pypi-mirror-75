"""Module contains CLI functions."""
import argparse
import pprint
from dataclasses import asdict

import httpx
from beer_keeper.client import BeerKeeper
from beer_keeper.custom_http_client import RealClient


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

    group = argument_parser.add_mutually_exclusive_group()

    group.add_argument(
        "-b",
        "--beer",
        type=int,
        action="store",
        help="Return a single beer by ID. Default beer=1.",
    )

    group.add_argument(
        "-ag",
        "--abv-greater",
        type=float,
        action="store",
        help="Return all beers with ABV greater than a given value.",
    )

    group.add_argument(
        "-al",
        "--abv-lower",
        type=float,
        action="store",
        help="Return all beers with ABV lower than a given value.",
    )

    group.add_argument(
        "-ig",
        "--ibu-greater",
        type=float,
        action="store",
        help="Return all beers with IBU greater than a given value.",
    )

    group.add_argument(
        "-il",
        "--ibu-lower",
        type=float,
        action="store",
        help="Return all beers with IBU lower than a given value.",
    )

    group.add_argument(
        "-p",
        "--page",
        type=int,
        action="store",
        help="Return all beers from page. Default page=1",
    )

    group.add_argument(
        "-r", "--random", action="store_true", help="Return a random beer",
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
    if arguments.random:
        return a_keeper.get_random_beer()
    elif arguments.page is not None:
        return a_keeper.get_all_beers_from_page(arguments.page, arguments.per_page)
    elif arguments.beer is not None:
        return a_keeper.get_beer(arguments.beer)
    elif arguments.abv_greater is not None:
        return a_keeper.get_beers_by_abv(arguments.abv_greater, greater=True)
    elif arguments.abv_lower is not None:
        return a_keeper.get_beers_by_abv(arguments.abv_lower, greater=False)
    elif arguments.ibu_greater is not None:
        return a_keeper.get_beers_by_ibu(arguments.ibu_greater, greater=True)
    elif arguments.ibu_lower is not None:
        return a_keeper.get_beers_by_ibu(arguments.ibu_lower, greater=False)
    else:
        return a_keeper.get_all_beers_from_page()


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
