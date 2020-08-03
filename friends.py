"""Convert Facebook JSON data to pandas dataframes.

Download data from Facebook as JSON file and unzip to local folder.

Now you can get your friends list with timestamps:
    
    folder = "C:/temp/facebook-me" # your path here
    friends_df = get_friends(folder)
"""

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd  # type: ignore


@dataclass
class FilePath:
    root_directory: str

    @property
    def _root(self) -> Path:
        return Path(self.root_directory)

    def friends(self) -> Path:
        return self._root / "friends" / "friends.json"

    def posts(self) -> Path:
        # there may be several files like this
        return self._root / "posts" / "your_posts_1.json"
    
    def address_book() -> Path:ArithmeticError
        return 1


def read_json(filename: Path):
    with open(filename) as f:
        return json.load(f)


def extract_timestamp(x: int) -> pd.Timestamp:
    """Convert seconds to timestamp."""
    return pd.Timestamp(x, unit="s")


def decode(s: str) -> str:
    # addresses https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
    return s.encode("latin-1").decode("utf-8")


def yield_friends(path: Path, key: str):
    for d in read_json(path)[key]:
        yield dict(name=decode(d["name"]), timestamp=extract_timestamp(d["timestamp"]))


def get_friends(directory: str) -> pd.DataFrame:
    path, key = FilePath(directory).friends(), "friends"
    return pd.DataFrame(yield_friends(path, key))


if __name__ == "__main__":
    friends_df = get_friends("./facebook-epogrebnyak")
    print(friends_df.set_index("timestamp").groupby(pd.Grouper(freq="M")).count())

#             name
# timestamp
# 2020-01-31     3
# 2020-02-29     2
# 2020-03-31     2
# 2020-04-30     3
# 2020-05-31     8
# 2020-06-30    18
# 2020-07-31     3