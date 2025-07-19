import json
import pathlib
from collections import OrderedDict
from enum import Enum
from typing import NewType

import polars as pl

"""
The Phaistos disc is inscribed on both sides in a spiral, and can be read a number of ways:
Sides A and B are so named by convention, but one could read them in the
reverse order. Additionally, researchers disagree as to whether the disc should
be read from the center outwards (left-to-right) or from the disc's edge toward
the center (right-to-left). This library provides facilities for reading in
either direction and for ordering the sides in either manner.
"""

DiscData = NewType("DiscData", OrderedDict[str, list[list[str]]])

data_fp = pathlib.Path(__file__).parents[0] / "data"
# side a -> side b outside in (right to left)
ab_oi_fp = data_fp / "phaistos-disc_outside-in.json"


def read_disc(disc_path: pathlib.Path = ab_oi_fp) -> DiscData:
    """Read a json formatted disc from file"""

    with open(disc_path, "r") as f:
        disc = json.loads(f.read())
    return disc


def read_sign_map(
    path: pathlib.Path = data_fp / "phaistos-disc_signs.csv",
) -> pl.DataFrame:
    sign_map: pl.DataFrame = pl.read_csv(path)
    return sign_map


class SideOrdering(Enum):
    a_b = ("side_a", "side_b")
    b_a = ("side_b", "side_a")


class Direction(Enum):
    ltr = "left-to-right"
    rtl = "right-to-left"
    inside_out = "left-to-right"
    outside_in = "right-to-left"


class OutputType(Enum):
    number = "No."
    symbol = "Symbol"
    unicode = "Unicode"
    phoneme = "Phoneme"


class PhaistosDisc:
    data: DiscData
    side_ordering: SideOrdering
    direction: Direction

    def __init__(
        self,
        data: DiscData = read_disc(),
        side_ordering: SideOrdering = SideOrdering.a_b,
        direction: Direction = Direction.rtl,
    ):
        """Initialize the disc with ordering, direction"""

        self.side_ordering = side_ordering
        self.direction = direction
        self.data = self.transpose(data, self.side_ordering, self.direction)

    def transpose(
        self,
        data: DiscData,
        side_ordering: SideOrdering = SideOrdering.a_b,
        direction: Direction = Direction.rtl,
    ) -> DiscData:
        ab = [
            ("side_a", data["side_a"]),
            ("side_b", data["side_b"]),
        ]
        if side_ordering == SideOrdering.a_b:
            self.data = OrderedDict(ab)
        else:
            self.data = OrderedDict(reversed(ab))

        # the data is stored in rtl (outside in)
        if direction == Direction.ltr:
            for side, val in self.data.items():
                # reverse the word order
                self.data[side] = list(reversed(self.data[side]))
                for i, word in enumerate(self.data[side]):
                    # reverse the characters in each word
                    self.data[side][i] = list(reversed(self.data[side][i]))
                    # the adfix symbol "," should follow its base
                    # symbol
                    if "46" in word:
                        idx = self.data[side][i].index("46")
                        (
                            self.data[side][i][idx],
                            self.data[side][i][idx + 1],
                        ) = (
                            self.data[side][i][idx + 1],
                            self.data[side][i][idx],
                        )

        return self.data

    def number_to_symbol(
        self, sign_map: pl.DataFrame, number: str, output_type: OutputType
    ):
        """Convert a zero-padded sign-number to unicode symbol or phonetic
        transcription.

        Phaistos symbols are numbered 01-47 according to standard interpretation.
        See ./src/data/phaistos-disc_signs.csv for complete listing.
        """

        sym = (
            sign_map.filter(pl.col("No.") == number)
            .select(output_type.value)
            .item()
        )
        return sym

    def format_disc(
        self,
        sign_map: pl.DataFrame = read_sign_map(),
        output_type: OutputType = OutputType.symbol,
        letter_separator: str = " ",
        word_separator: str = "\n",
        prefix: bool = True,
    ) -> str:
        """Format the phaistos disc into a string using {output_type}"""

        sides = self.data.keys()
        output = []
        for side in sides:
            side_letter = side[-1].upper()
            for i, word in enumerate(self.data[side]):
                symbols = [
                    self.number_to_symbol(sign_map, sign, output_type)
                    for sign in word
                ]
                _prefix = f"{side_letter}{i + 1} " if prefix else ""
                output.append(f"{_prefix}{letter_separator.join(symbols)}")
        return word_separator.join(output)
