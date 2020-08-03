"""Convert Facebook JSON data to pandas dataframes.

Download data from Facebook as JSON file and unzip to local folder.

Now you can get your friends list with timestamps:
    
    folder = "C:/temp/facebook-me" # your path here
    friends_df = get_friends(folder)
"""

import json
from dataclasses import dataclass
from pathlib import Path
import datetime

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

    def address_book(self) -> Path:
        return self._root / "about_you" / "your_address_books.json"


def read_json(filename: Path):
    with open(filename) as f:
        return json.load(f)


def extract_timestamp(x: int) -> datetime.datetime:
    """Convert seconds to timestamp."""
    return datetime.datetime.fromtimestamp(x) 


def decode(s: str) -> str:
    # addresses https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
    return s.encode("latin-1").decode("utf-8")


def yield_friends(path: Path, key: str):
    for d in read_json(path)[key]:
        yield dict(name=decode(d["name"]), timestamp=extract_timestamp(d["timestamp"]))


def get_friends(directory: str):
    path, key = FilePath(directory).friends(), "friends"
    return list(yield_friends(path, key))


def _get_details(d: dict) -> str:
    try:
        return d["details"][0]["contact_point"]
    except IndexError:
        return ""


def yield_address_book(path: Path):
    for d in read_json(path)["address_book"]["address_book"]:
        yield dict(name=decode(d["name"]), contact_point=_get_details(d))


def get_address_book(directory: str):
    path = FilePath(directory).address_book()
    return list(yield_address_book(path))

if __name__ == "__main__":    
    import pandas as pd  # type: ignore    

    folder = "./facebook-epogrebnyak"
    friends = get_friends(folder)
    print("Friends added in Jan-Jul 2020:", len(friends))
    # Friends added in Jan-Jul 2020: 39
    
    print("By month:")
    friends_df = pd.DataFrame(friends).set_index("timestamp")
    print(friends_df.groupby(pd.Grouper(freq="M")).count())
    # By month:
    #             name
    # timestamp
    # 2020-01-31     3
    # 2020-02-29     2
    # 2020-03-31     2
    # 2020-04-30     3
    # 2020-05-31     8
    # 2020-06-30    18
    # 2020-07-31     3

    phones = get_address_book(folder)
    print("\nNumbers from my phonebook on Facebook:", len(phones))
    # Numbers from my phonebook Facebook stores: 

