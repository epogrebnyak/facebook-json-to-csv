"""Convert Facebook JSON data to plain format for data analysis.

Download data from Facebook as JSON file and unzip to local folder.

Now you can get your friends list with timestamps 
and your phone numbers stored by Facebook:
    
    folder = "C:/temp/facebook-me" # your path here
    friends = get_friends(folder)
    phones =  get_address_book(folder)
"""

import json
from dataclasses import dataclass
from pathlib import Path
import datetime


__all__ = ["get_friends", "get_address_book"]


@dataclass
class FilePath:
    directory: str

    @property
    def root(self) -> Path:
        return Path(self.directory)

    def friends(self) -> Path:
        return self.root / "friends" / "friends.json"

    def posts(self) -> Path:
        # there may be several files like this
        return self.root / "posts" / "your_posts_1.json"

    def address_book(self) -> Path:
        return self.root / "about_you" / "your_address_books.json"


def filepath(directory, attrib):
    return getattr(FilePath(directory), attrib)()


def get(directory, attrib, yield_func):
    d = read_json(filepath(directory, attrib))
    return list(yield_func(d))


def read_json(filename: Path):
    with open(filename) as f:
        return json.load(f)


def extract_timestamp(x: int) -> datetime.datetime:
    """Convert seconds to timestamp."""
    return datetime.datetime.fromtimestamp(x)


def decode(s: str) -> str:
    # addresses https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
    return s.encode("latin-1").decode("utf-8")


def yield_friends(xs):
    for d in xs["friends"]:
        yield dict(name=decode(d["name"]), timestamp=extract_timestamp(d["timestamp"]))


def get_friends(directory: str):
    return get(directory, "friends", yield_friends)


def extract_details(d: dict) -> str:
    try:
        return d["details"][0]["contact_point"]
    except IndexError:
        return ""


from typing import Callable

@dataclass
class Getter:    
    access_with : Callable = lambda xs: xs
    extract : Callable = lambda x: x    
    

def yield_address_book(xs):
    for x in xs["address_book"]["address_book"]:
        yield dict(name=decode(x["name"]), contact_point=extract_details(x))


def get_address_book(directory: str):
    return get(directory, "address_book", yield_address_book)


def extract_post(d: dict) -> str:
    try:
        return decode(d["data"][0]["post"])
    except KeyError:
        return ""


def yield_posts(xs):
    for x in xs:
        yield dict(post=extract_post(x), timestamp=extract_timestamp(x["timestamp"]))


def get_posts(directory: str):
    return get(directory, "posts", yield_posts)


if __name__ == "__main__":
    import pandas as pd  # type: ignore

    def cnt(items):
        return (
            pd.DataFrame(items)
            .set_index("timestamp")
            .groupby(pd.Grouper(freq="M"))
            .count()
        )

    folder = "./facebook-epogrebnyak"
    friends = get_friends(folder)
    print("Friends added in Jan-Jul 2020:", len(friends))
    # Friends added in Jan-Jul 2020: 39

    friends_df = pd.DataFrame(friends)
    print("By month:", cnt(friends))
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

    posts = get_posts(folder)
    print("\nNumbers of posts Jan-Jul 2020:", len(posts))
    print("By month:\n", cnt(posts))

# TODO - things to try:
# - Enforce dataframe properties via pandera or bulwark
# - Generate fake data and folder stucture for testing
# - Add post, comments, locations
