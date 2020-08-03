"""Convert Facebook JSON data to pandas dataframes.

Download data from Facebook as JSON file and unzip to local folder.

Now you can get your friends list with timestamps:
    
    folder = "c:/temp/facebook-me" # your path here
    friends_df = get_friends(folder)
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd  # type: ignore


@dataclass
class FilePath:
    root_dir_str: str

    @property
    def root_dir(self) -> Path:
        return Path(self.root_dir_str)

    def friends(self) -> Tuple[Path, str]:
        return self.root_dir / "friends" / "friends.json", "friends"


def read_json(filename: Path) -> dict:
    with open(filename) as f:
        return json.load(f)


def get_timestamp(x: int) -> pd.Timestamp:
    """Convert seconds to timestamp.    
    >>> get_timestamp(1582964988)
    Timestamp('2020-02-29 08:29:48')
    """
    return pd.Timestamp(x, unit="s")


def decode(s: str) -> str:
    return s.encode("latin-1").decode("utf-8")


def friends_dict_to_dataframe(source_dict: dict, key: str) -> pd.DataFrame:
    df = pd.DataFrame(source_dict[key])
    df["name"] = df["name"].map(decode)
    df["timestamp"] = df["timestamp"].map(get_timestamp)
    return df.set_index("timestamp")


def get_friends(directory: str) -> pd.DataFrame:
    path, key = FilePath(directory).friends()
    return friends_dict_to_dataframe(read_json(path), key)


if __name__ == "__main__":
    friends_df = get_friends(".")
    print(friends_df.groupby(pd.Grouper(freq="M")).count())

#             name
# timestamp
# 2020-01-31     3
# 2020-02-29     2
# 2020-03-31     2
# 2020-04-30     3
# 2020-05-31     8
# 2020-06-30    18
# 2020-07-31     3
