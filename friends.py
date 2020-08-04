"""Convert Facebook JSON data to plain format for data analysis.

Download data from Facebook as JSON file and unzip to local folder,
like "C:/temp/facebook-me".

Now you can get your friends list with timestamps and your phone 
numbers stored by Facebook as well as posts:
    
    from friends import get_friends, get_address_book, get_posts
    
    directory = "C:/temp/facebook-me" # your path to folder with JSON here
    friends = get_friends(directory)
    phones = get_address_book(directory)
    posts = get_posts(directory)

"""

import datetime
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

__all__ = ["get_friends", "get_address_book", "get_posts", "get_comments"]


@dataclass
class Getter:
    path: List[str]
    unpack: Callable
    elem: Callable
    columns: List[str]

    def make_path(self, directory):
        return Path(directory).joinpath(*self.path)

    def iterate(self, directory):
        path = self.make_path(directory)
        xs = read_json(path)
        for x in self.unpack(xs):
            yield self.elem(x)

    def get(self, directory):
        return list(self.iterate(directory))

    def get_dataframe(self, directory):
        import pandas as pd # type: ignore

        df = pd.DataFrame(self.iterate(directory), columns=self.columns)
        if "timestamp" in self.columns:
            df["timestamp"] = df.timestamp.map(lambda x: pd.Timestamp(x, unit="s"))
        return df
    

def get_list(directory, fb_item):
    return fb_item.get(directory)
    
def iterate(directory, fb_item):
    return fb_item.iterate(directory)

def get_dataframe(directory, fb_item):
    return fb_item.get_dataframe(directory)



class FB:
    comments = Getter(
        path=["comments", "comments.json"],
        unpack=lambda xs: xs["comments"],
        elem=lambda x: (x["timestamp"], decode(x["data"][0]["comment"]["comment"])),
        columns=["timestamp", "comment"],
    )

    friends = Getter(
        path=["friends", "friends.json"],
        unpack=lambda xs: xs["friends"],
        elem=lambda x: (x["timestamp"], decode(x["name"]),),
        columns=["timestamp", "name"],
    )

    posts = Getter(
        # maybe there are several files for posts
        path=["posts", "your_posts_1.json"],
        unpack=lambda xs: xs,
        elem=lambda x: (x["timestamp"], extract_post(x),),
        columns=["timestamp", "post"],
    )

    address_book = Getter(
        path=["about_you", "your_address_books.json"],
        unpack=lambda xs: xs["address_book"]["address_book"],
        elem=lambda x: (decode(x["name"]), extract_address_book_details(x)),
        columns=["name", "contact"],
    )


def get_address_book(directory: str):
    return FB.address_book.get(directory)


def get_friends(directory: str):
    return FB.friends.get(directory)


def get_posts(directory: str):
    return FB.posts.get(directory)


def get_comments(directory: str):
    return FB.comments.get(directory)


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


def extract_address_book_details(d: dict) -> str:
    try:
        return d["details"][0]["contact_point"]
    except IndexError:
        return ""


def extract_post(d: dict) -> str:
    try:
        return decode(d["data"][0]["post"])
    except KeyError:
        return ""


def tprint(labels, values, **kwargs):
    # See https://github.com/mkaz/termgraph/issues/27
    from termgraph.termgraph import chart # type: ignore

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

    def count(df_):
        df = df_.set_index("timestamp").groupby(pd.Grouper(freq="M")).count()
        df.index.name = None
        df.columns = [""]
        df.index = df.index.to_period("M")
        return df

    def print_count(df):
        df = count(df)
        tprint(
            [str(x) for x in df.index],
            df.iloc[:, 0].tolist(),
            format="{:<5.0f}",
            width=20,
        )

    directory = "./facebook-epogrebnyak"
    friends = get_friends(directory)
    print("Friends added in Jan-Jul 2020 by month (total %i)" % len(friends))
    friends_df = FB.friends.get_dataframe(directory)
    print_count(friends_df)

    phones = get_address_book(directory)
    print("\nContacts from my phonebook stored by Facebook:")
    tprint(["2020-07"], [len(phones)], format="{:d}")

    posts = get_posts(directory)
    print("\nNumber of posts Jan-Jul 2020 by month (total %i)" % len(posts))
    posts_df = FB.posts.get_dataframe(directory)
    print_count(posts_df)

# TODO - things to try:

# Implementation:
# - Enforce dataframe properties via pandera or bulwark
# - Generate fake data and folder stucture for testing
# - Installable package (poetry?)


# Functionality:
# - [x] text-based graphs
# - add comments, locations retieval - new get_something() functions
# - output directory for CSVs
