"""
The Phaistos disc is inscribed on both sides in a spiral, and can be read a number of ways:
Sides A and B are so named by convention, but one could read them in the
reverse order. Additionally, researchers disagree as to whether the disc should
be read from the center outwards (left-to-right) or from the disc's edge toward
the center (right-to-left). This library provides facilities for reading in
either direction and for ordering the sides in either manner.
"""

from collections import OrderedDict

import polars as pl

from phaistos_disc.util import (
    DiscData,
    StrEnum,
    number_to_symbol,
    read_disc,
    read_sign_map,
)


class SideOrdering(StrEnum):
    a_b = "a_b"
    b_a = "b_a"


class Direction(StrEnum):
    ltr = "left-to-right"
    rtl = "right-to-left"
    inside_out = "left-to-right"
    outside_in = "right-to-left"


class OutputType(StrEnum):
    number = "number"
    symbol = "symbol"
    unicode = "unicode"
    phoneme = "phoneme"


class PhaistosDisc:
    data: DiscData
    side_ordering: SideOrdering | str
    direction: Direction | str

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
                    number_to_symbol(sign_map, sign, output_type)
                    for sign in word
                ]
                _prefix = f"{side_letter}{i + 1} " if prefix else ""
                output.append(f"{_prefix}{letter_separator.join(symbols)}")
        return word_separator.join(output)

    def get_stats(self):
        """Provides lexical statistics for the disc"""

        words = []
        glyphs = []
        for side, value in self.data.items():
            for word in value:
                _word = " ".join(word)
                words.append(_word)
                for glyph in word:
                    glyphs.append(glyph)

        glyphs_df = pl.DataFrame({"glyph": glyphs})
        glyphs_df = (
            glyphs_df.group_by("glyph")
            .agg(pl.len().alias("count"))
            .sort("count", descending=True)
        )

        words_df = pl.DataFrame({"word": words})
        words_df = (
            words_df.group_by("word")
            .agg(pl.len().alias("count"))
            .sort("count", descending=True)
        )
        return glyphs_df, words_df
