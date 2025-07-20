from __future__ import annotations

import json
import pathlib
from collections import OrderedDict
from enum import Enum
from typing import NewType

import polars as pl

data_fp = pathlib.Path(__file__).parents[0] / "data"


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


DiscData = NewType("DiscData", OrderedDict[str, list[list[str]]])

# side a -> side b outside in (right to left)
ab_oi_fp = data_fp / "phaistos-disc_outside-in.json"


def read_disc(disc_path: pathlib.Path = ab_oi_fp) -> DiscData:
    """Read a json formatted disc from file"""
    with open(disc_path, "r") as f:
        disc = json.loads(f.read())
    return disc


sign_map_schema = {
    "number": pl.String,
    "symbol": pl.String,
    "name": pl.String,
    "unicode": pl.String,
    "phoneme": pl.String,
}


def read_sign_map(
    path: pathlib.Path = data_fp / "phaistos-disc_signs.csv",
) -> pl.DataFrame:
    """Read a csv from path and create a DataFrame.
    Fill in missing columns, rename columns as appropriate.

    Return a polars DataFrame
    """
    sign_map: pl.DataFrame = pl.read_csv(
        path,
        schema=sign_map_schema,
    )
    return sign_map


def number_to_symbol(
    sign_map: pl.DataFrame,
    number: str,
    output_type: "OutputType" | str,  # noqa: F821
) -> str:
    """Convert a zero-padded sign-number to unicode symbol or phonetic
    transcription.

    Phaistos symbols are numbered [01-47) according to standard interpretation.
    See ./src/phaistos_disc/data/phaistos-disc_signs.csv for complete listing.
    """

    sym = (
        sign_map.filter(pl.col("number") == number).select(output_type).item()
    )
    return sym
