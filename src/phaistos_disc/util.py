import json
import pathlib
from enum import Enum

import pandas as pd

data_fp = pathlib.Path(__file__).parents[1] / "data"


class DiscToPath(Enum):
    """The Phaistos disc can be read a number of ways:
    Sides A and B are so named by convention, but one could read them in the
    reverse order. Additionally, researchers disagree whether the disc should
    be read from the center outwards (left-to-right) or from the disc's edge
    toward the center (right-to-left). This library provides both readings in
    ./src/data/ . This enum is a helper tool for accessing either
    interpretation.
    """

    inside_out = data_fp / "phaistos-disc_inside-out.json"
    outside_in = data_fp / "phaistos-disc_outside-in.json"


def get_sign_map(
    path: pathlib.Path = data_fp / "phaistos-disc_signs.csv",
):
    sign_map: pd.DataFrame = pd.read_csv(path, index_col="No.", dtype="string")
    return sign_map


def read_disc(disc_path: pathlib.Path):
    """Read a json formatted disc from file"""

    with open(disc_path, "r") as f:
        disc = json.loads(f.read())
    return disc


class OutputType(Enum):
    number = "No."
    symbol = "Symbol"
    unicode = "Unicode"
    phoneme = "Phoneme"


def number_to_symbol(
    sign_map: pd.DataFrame, number: str, output_type: OutputType
):
    """Convert a zero-padded sign-number to unicode symbol.
    Phaistos symbols are numbered 01-47 according to standard interpretation.
    See ./src/data/phaistos-disc_signs.csv for complete listing.
    """

    return sign_map.loc[number][output_type.value]


def format_disc(
    disc: DiscToPath | pathlib.Path,
    sign_map=get_sign_map(),
    output_type: OutputType = OutputType.symbol,
    letter_separator: str = " ",
    word_separator: str = "\n",
    prefix: bool = True,
):
    """Print a disc with unicode symbols with Side+wordcount prefix"""
    disc_path = DiscToPath[disc].value
    disc = read_disc(disc_path)
    sides = disc.keys()
    output = []
    for side in sides:
        side_letter = side[-1].upper()
        for i, word in enumerate(disc[side]):
            symbols = [
                number_to_symbol(sign_map, sign, output_type) for sign in word
            ]
            _prefix = f"{side_letter}{i+1} " if prefix else ""
            output.append(f"{_prefix}{letter_separator.join(symbols)}")
    return word_separator.join(output)


if __name__ == "__main__":
    # print_disc("outside_in")
    # formatted_disc = format_disc(
    #     "inside_out",
    #     letter_separator="-",
    #     word_separator="|",
    #     prefix=False,
    # )
    # print(formatted_disc)

    achterberg_transcription = format_disc(
        "outside_in",
        sign_map=get_sign_map(data_fp / "phaistos-disc_signs-achterberg.csv"),
        output_type=OutputType.phoneme,
        letter_separator="-",
        word_separator="\n",
        prefix=True,
    )
    print(achterberg_transcription)
