"""Functions used for the new parameters specification method."""
from datetime import datetime
from enum import Enum
from typing import List
from typing import Tuple


def greater_than(value: int) -> Tuple[str, int]:
    """
    Use when parameter condition is greater_than.

    Parameters
    ----------
    value : int
        Reference value.

    Returns
    -------
    Tuple[str, int]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    return ("_gt", value)


def less_than(value: int) -> Tuple[str, int]:
    """
    Use when parameter condition is less_than.

    Parameters
    ----------
    value : int
        Reference value.

    Returns
    -------
    Tuple[str, int]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    return ("_lt", value)


def before(value: datetime) -> Tuple[str, str]:
    """
    Use when parameter condition is before.

    Parameters
    ----------
    value : datetime
        Reference value.

    Returns
    -------
    Tuple[str, str]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    month_year = ""
    month_year += str(value.month)
    month_year += "-"
    month_year += str(value.year)
    return ("_before", month_year)


def after(value: datetime) -> Tuple[str, str]:
    """
    Use when parameter condition is after.

    Parameters
    ----------
    value : datetime
        Reference value.

    Returns
    -------
    Tuple[str, str]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    month_year = ""
    month_year += str(value.month)
    month_year += "-"
    month_year += str(value.year)
    return ("_after", month_year)


def equals(value: str) -> Tuple[str, int]:
    """
    Use when parameter condition is equals.

    Parameters
    ----------
    value : int
        Reference value.

    Returns
    -------
    Tuple[str, int]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    return ("", value)


def inside(value: List[int]) -> Tuple[str, str]:
    """
    Use when parameter condition is inside.

    Parameters
    ----------
    value : List[int]
        Reference values.

    Returns
    -------
    Tuple[str, str]
        Tuple in which the first position is used to build query param and the second position is used as the value for the query param.
    """
    s = "(|"
    for id in value:
        s += str(id)
        s += "|"
    s += ")"
    return ("", s)
    # (|1|)


class P:
    """Represent a parameter object, along with the condition applied on it."""

    def __init__(
        self, keyword_param, condition: Tuple = None, conditions: list = None,
    ):
        self.keyword_param = keyword_param
        self.condition = condition
        self.conditions = conditions

    def get_all_conditions(self) -> List[tuple]:
        """
        Build a list with all the conditions of the parameter object.

        Returns
        -------
        list[tuple]
            The list that was built.
        """
        conditions = []
        if self.condition is not None:
            conditions.append(self.condition)
        if self.conditions is not None:
            for cond in self.conditions:
                conditions.append(cond)
        return conditions


class Param(Enum):
    """Parameter class for query paramaters."""

    abv = "abv"
    ibu = "ibu"
    ebc = "ebc"
    beer_name = "beer_name"
    yeast = "yeast"
    brewed = "brewed"
    hops = "hops"
    malt = "malt"
    food = "food"
    ids = "ids"
    page = "page"
    per_page = "per_page"

    def __str__(self):
        """
        Use this instead of Param.attribute.value.

        Returns
        -------
        str
        """
        return str(self.value)
