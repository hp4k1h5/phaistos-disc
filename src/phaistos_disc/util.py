import json
import pathlib

import pandas as pd

data_fp = pathlib.Path(__file__).parents[1] / "data"

disc_to_path = {
    "inside_out": data_fp / "phaistos-disc_inside-out.json",
    "outside_in": data_fp / "phaistos-disc_outside-in.json",
}
sign_map = pd.read_csv(
    data_fp / "phaistos-disc_signs.csv", index_col="No.", dtype="string"
)


def read_disc(disc_path):
    with open(disc_path, "r") as f:
        disc = json.loads(f.read())
    return disc


def sign_to_word(sign_map: pd.DataFrame, number: str):
    return sign_map.loc[number]["Symbol"]


def print_disc(disc):
    disc_path = disc_to_path[disc]
    disc = read_disc(disc_path)
    sides = "side_a", "side_b"
    for side in sides:
        side_letter = side[-1].upper()
        for i, word in enumerate(disc[side]):
            symbols = [sign_to_word(sign_map, sign) for sign in word]
            print(f"{side_letter}{i+1} {' '.join(symbols)}")


if __name__ == "__main__":
    ...
    # print_disc("outside_in")
    print_disc("inside_out")
    # disc = read_disc(disc_to_path["inside_out"])
    # sides = "side_a", "side_b"
    # for side in sides:
    #     for i, word in enumerate(disc[side]):
    #         if "46" in word:
    #             word[0:2] = list(reversed(word[0:2]))
    #
    # with open(disc_to_path["inside_out"], "w") as f:
    #     f.write(json.dumps(disc))
