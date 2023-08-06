"""Beer dataclass."""
import typing
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Beer:
    """Class for keeping track of beer characteristics."""

    id: int
    name: str
    tagline: str
    first_brewed: str
    description: str
    image_url: str
    abv: float
    ibu: float
    target_fg: float
    target_og: float
    ebc: float
    srm: float
    ph: float
    attenuation_level: float
    volume: typing.Dict
    boil_volume: typing.Dict
    method: typing.Dict
    ingredients: typing.Dict
    food_pairing: list
    brewers_tips: str
    contributed_by: str
