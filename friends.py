"""Convert Facebook JSON data to plain format for data analysis.

Download data from Facebook as JSON file and unzip to local folder.

Now you can get your friends list with timestamps and your phone 
numbers stored by Facebook as well as posts:
    
    directory = "C:/temp/facebook-me" # your path here
    friends = get_friends(directory)
    phones = get_address_book(directory)
    posts = get_posts(directory)

"""

import datetime
import json
from pathlib import Path
from typing import Dict, List

__all__ = ["get_friends", "get_address_book", "get_posts"]


def path_friends(directory: str) -> Path:
    return Path(directory) / "friends" / "friends.json"


# maybe there are several files for posts
def path_posts(directory: str) -> Path:
    return Path(directory) / "posts" / "your_posts_1.json"


# maybe there are several files for posts
def path_address_book(directory: str) -> Path:
    return Path(directory) / "about_you" / "your_address_books.json"


def read_json(filename: Path):
    with open(filename) as f:
        return json.load(f)


def extract_timestamp(x: int) -> datetime.datetime:
    """Convert seconds to timestamp."""
    return datetime.datetime.fromtimestamp(x)


def decode(string: str) -> str:
    """Return *string* in readable view.
    
    Addresses this issue:
    https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
    
    """
    return string.encode("latin-1").decode("utf-8")


def yield_friends(xs: Dict):
    for x in xs["friends"]:
        yield dict(name=decode(x["name"]), timestamp=extract_timestamp(x["timestamp"]))


def get_friends(directory: str):
    return get_list(directory, path_friends, yield_friends)


def extract_address_book_details(d: dict) -> str:
    try:
        return d["details"][0]["contact_point"]
    except IndexError:
        return ""


def yield_address_book(xs: Dict):
    for x in xs["address_book"]["address_book"]:
        yield dict(
            name=decode(x["name"]), contact_point=extract_address_book_details(x)
        )


def get_address_book(directory: str):
    return get_list(directory, path_address_book, yield_address_book)


def extract_post(d: dict) -> str:
    try:
        return decode(d["data"][0]["post"])
    except KeyError:
        return ""


def yield_posts(xs: List):
    for x in xs:
        yield dict(post=extract_post(x), timestamp=extract_timestamp(x["timestamp"]))


def get_posts(directory: str):
    return get_list(directory, path_posts, yield_posts)


def get_list(directory, path_func, yield_func):
    path = path_func(directory)
    xs = read_json(path)
    gen = yield_func(xs)
    return list(gen)


def tprint(labels, values, **kwargs):
    # See https://github.com/mkaz/termgraph/issues/27
    from termgraph.termgraph import chart

    args = {
        "stacked": False,
        "width": 50,
        "no_labels": False,
        "format": "{:<5.2f}",
        "suffix": "",
        "vertical": False,
        "histogram": False,
        "no_values": False,
    }
    args.update(kwargs)
    data = [[x] for x in values]
    chart(colors=[], data=data, args=args, labels=labels)


if __name__ == "__main__":
    import pandas as pd  # type: ignore

    def count(items):
        df = (
            pd.DataFrame(items)
            .set_index("timestamp")
            .groupby(pd.Grouper(freq="M"))
            .count()
        )
        df.index.name = None
        df.columns = [""]
        df.index = df.index.to_period("M")
        return df

    def print_count(items):
        df = count(items)
        tprint([str(x) for x in df.index], df.iloc[:, 0].tolist(), 
               format="{:<5.0f}", width=20)

    directory = "./facebook-epogrebnyak"
    friends = get_friends(directory)
    friends_df = pd.DataFrame(friends)
    print("Friends added in Jan-Jul 2020 by month (total %i)" % len(friends))
    print_count(friends)

    phones = get_address_book(directory)
    print("\nContacts from my phonebook stored by Facebook:")
    tprint(["2020-07"], [len(phones)], format="{:d}")

    posts = get_posts(directory)
    print(
        "\nNumber of posts Jan-Jul 2020 by month (total %i)" % len(posts))
    print_count(posts)

# TODO - things to try:
# - Enforce dataframe properties via pandera or bulwark
# - Generate fake data and folder stucture for testing
# - Add comments, locations
# - CLI graphs
# - output directory for CSVs
