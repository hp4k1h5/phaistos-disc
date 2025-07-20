import pathlib

import polars as pl

from phaistos_disc.model import OutputType
from phaistos_disc.util import read_sign_map

data_fp = pathlib.Path(__file__).parents[0] / "data"


def test_read_sign_map():
    sm = read_sign_map(data_fp / "sign_map_ok.csv")
    assert type(sm) is pl.DataFrame


def test_read_sign_map_err():
    sm = read_sign_map(data_fp / "sign_map_err.csv")
    assert type(sm) is pl.DataFrame


def test_str_enum():
    """Enums should be str equivalent"""
    assert OutputType.number == "number"
    df = pl.DataFrame({"number": 0})
    assert df.select("number").equals(df.select(OutputType.number))
