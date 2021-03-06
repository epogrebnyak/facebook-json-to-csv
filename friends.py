"""Convert Facebook JSON data to plain format for data analysis.

Download data from Facebook as JSON file and unzip to local folder,
like "C:/temp/facebook-me".

Now you can get your friends list with timestamps and your phone 
numbers stored by Facebook as well as posts.

The easiest way to access data is get_something() functions:
    
    from friends import get_friends, get_address_book, get_posts
    
    directory = "C:/temp/facebook-me" # your path to folder with JSON here
    friends = get_friends(directory)
    phones = get_address_book(directory)
    posts = get_posts(directory)

The functions about return lists. You may want to work with generators
of tuples or dicts or pandas dataframes as well. You can use reader 
classes for that:

    from friends import Friends, Comments, Posts, AddressBook 
    
    f = Friends("./facebook-epogrebnyak")
    friends = f.get_tuples()         # list of (timestamp, name) tuples
    friends_dicts = f.get_dicts()    # same data as list of dictionaries
    friends_gen = f.iterate()        # useful for streaming large archives
    friends_df = f.get_dataframe()   # pandas DataFrame ready for analysis 
    f.save_csv("./output_folder")    # saves data to 'friends.csv'

"""

import datetime
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List


__all__ = [
    "save_csv_all" "get_friends",
    "Friends",
    "get_address_book",
    "AddressBook",
    "get_posts",
    "Posts",
    "get_comments",
    "Comments",
    "get_reactions",
    "Reactions",
    "get_sessions",
    "Sessions",
]


@dataclass
class Getter:
    name: str
    # file location inside JSON folder
    path: List[str]
    # access specific part of file after reading it by read_json()
    unpack: Callable
    # convert one element (eg post, comment) to final representation
    elem: Callable
    columns: List[str]

    def make_path(self, directory):
        return Path(directory).joinpath(*self.path)

    def iterate(self, directory):
        path = self.make_path(directory)
        xs = read_json(path)
        for x in self.unpack(xs):
            yield self.elem(x)


class FB:
    """Getter classes by types of content."""

    address_book = Getter(
        name="address_book",
        path=["about_you", "your_address_books.json"],
        unpack=lambda xs: xs["address_book"]["address_book"],
        elem=lambda x: (decode(x["name"]), extract_address_book_details(x)),
        columns=["name", "contact"],
    )

    friends = Getter(
        name="friends",
        path=["friends", "friends.json"],
        unpack=lambda xs: xs["friends"],
        elem=lambda x: (x["timestamp"], decode(x["name"]),),
        columns=["timestamp", "name"],
    )

    posts = Getter(
        name="posts",
        # maybe there are several files for posts
        path=["posts", "your_posts_1.json"],
        unpack=lambda xs: xs,
        elem=lambda x: (x["timestamp"], extract_post(x),),
        columns=["timestamp", "content"],
    )

    comments = Getter(
        name="comments",
        path=["comments", "comments.json"],
        unpack=lambda xs: xs["comments"],
        elem=lambda x: (x["timestamp"], decode(x["data"][0]["comment"]["comment"])),
        columns=["timestamp", "content"],
    )

    reactions: Getter = Getter(
        name="reactions",
        path=["likes_and_reactions", "posts_and_comments.json"],
        unpack=lambda xs: xs["reactions"],
        elem=lambda x: (
            x["timestamp"],
            x["data"][0]["reaction"]["reaction"],
            decode(x["title"]),
        ),
        columns=["timestamp", "reaction", "title"],
    )

    sessions: Getter = Getter(
        name="sessions",
        path=["security_and_login_information", "account_activity.json"],
        unpack=lambda xs: xs["account_activity"],
        elem=lambda x: (
            x["timestamp"],
            x["ip_address"],
            decode(x["city"]),
            decode(x["region"]),
            x["country"],
        ),
        columns=["timestamp", "ip_address", "city", "region", "ip_address"],
    )


class Reader:
    """Parent class to associate specific *directory* and Getter."""

    getter: Getter = None

    def __init__(self, directory: str):
        self.directory = directory

    @property
    def columns(self):
        return self.getter.columns

    def iterate(self):
        return self.getter.iterate(self.directory)

    def get_tuples(self):
        return list(self.iterate())

    def yield_dicts(self):
        for values in self.iterate():
            yield dict(zip(self.columns, values))

    def get_dicts(self):
        return list(self.yield_dicts())

    def get_dataframe(self):
        import pandas as pd  # type: ignore

        df = pd.DataFrame(self.iterate(), columns=self.columns)
        if "timestamp" in self.columns:
            df["timestamp"] = df.timestamp.map(lambda x: pd.Timestamp(x, unit="s"))
        return df

    @classmethod
    def csv_path(cls, output_dir):
        return Path(output_dir) / (cls.getter.name + ".csv")

    def save_csv(self, output_dir):
        df = self.get_dataframe()
        filepath = self.csv_path(output_dir)
        df.to_csv(filepath, index=None)
        return filepath


def save_csv_all(source_dir: str, output_dir: str):
    filepaths = []
    for reader in Reader.__subclasses__():
        fp = reader(source_dir).save_csv(output_dir)
        filepaths.append(fp)
    print("\nSaved files:\n ", "\n  ".join(map(str, filepaths)))
    return filepaths


class Friends(Reader):
    getter = FB.friends


class Comments(Reader):
    getter = FB.comments


class Posts(Reader):
    getter = FB.posts


class AddressBook(Reader):
    getter = FB.address_book


class Reactions(Reader):
    getter = FB.reactions


class Sessions(Reader):
    getter = FB.sessions


def all_getters():
    return [getattr(FB, k) for k in FB.__dict__.keys() if not k.startswith("_")]


def get_address_book(directory: str):
    return AddressBook(directory).get_tuples()


def get_friends(directory: str):
    return Friends(directory).get_tuples()


def get_posts(directory: str):
    return Posts(directory).get_tuples()


def get_comments(directory: str):
    return Comments(directory).get_tuples()


def get_reactions(directory: str):
    return Reactions(directory).get_tuples()


def get_sessions(directory: str):
    return Sessions(directory).get_tuples()


def read_json(filename: Path):
    with open(filename) as f:
        return json.load(f)


# not in use now
def extract_timestamp(x: int) -> datetime.datetime:
    """Convert seconds to timestamp."""
    return datetime.datetime.fromtimestamp(x)


def decode(string: str) -> str:
    """Return *string* in readable view.
    
    Facebook encodes utf as latin-1 making non-latin 
    chars unreadable. See:
        
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
    from termgraph.termgraph import chart  # type: ignore

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
        df.index = df.index.to_period("M")
        return df

    def print_count(df_):
        df = count(df_)
        tprint(
            [str(x) for x in df.index],
            df.iloc[:, 0].tolist(),
            format="{:<5.0f}",
            width=20,
        )

    directory = "./facebook-epogrebnyak"

    phones = get_address_book(directory)
    print("\nContacts from my phonebook stored by Facebook:")
    tprint(["Total"], [len(phones)], format="{:d}")

    friends = get_friends(directory)
    print("Friends added by month (total %i)" % len(friends))
    friends_df = Friends(directory).get_dataframe()
    print_count(friends_df)

    comments_df = Comments(directory).get_dataframe()
    posts_df = Posts(directory).get_dataframe()
    pubs_df = pd.concat([posts_df, comments_df])
    print("\nNumber of posts and comments by month (total %i)" % len(pubs_df))
    print_count(pubs_df)

    reactions_df = Reactions(directory).get_dataframe()
    print("\nReactions by month (total %i)" % len(reactions_df))
    print_count(reactions_df)

    sessions_df = Sessions(directory).get_dataframe()
    print("\nSessions by month (total %i)" % len(sessions_df))
    print_count(sessions_df)
    print(
        "Session locations (includes VPN):",
        ", ".join(sorted(sessions_df.city.unique().tolist())),
    )

    f = Friends(directory)
    friends_list = f.get_tuples()  # returns list of tuples
    friends_dicts = f.get_dicts()  # returns list of dictionaries
    friends_gen = f.iterate()  # useful for streaming large archives
    friends_df = f.get_dataframe()  # ready for analysis
    f.save_csv("./output_folder")

    filepaths = save_csv_all(
        source_dir="./facebook-epogrebnyak", output_dir="./output_folder"
    )


# TODO - things to try:

# Implementation:
# - Enforce dataframe properties via pandera or bulwark
# - Generate fake data and folder stucture for testing
# - Installable package (via poetry?)
# - Rename package and project
# - Test on large archive (~1GB)
# - Logging strategy

# Functionality:
# - [x] text-based graphs
# - [x] output directory for CSVs
# - save all files as CSV
# - largest files in the directory - see  `tree --sort=size -s .`
# - own jpegs in posts

# Content:
# - all links ever mentioned in posts
# - FB Messenger messages

# Probably cannot do that:
# - all posts where I'm tagged
# - face recognition data (useless)
